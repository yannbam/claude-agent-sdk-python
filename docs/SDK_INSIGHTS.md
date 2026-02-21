# SDK Insights

Non-obvious learnings from exploring the Claude Agent SDK. High-signal, concise, self-contained. Append as we go.

---

## CLI Discovery (2026-01-10)

The SDK doesn't contain Claude — it spawns the Claude Code CLI as a subprocess.

**Discovery order** (`_internal/transport/subprocess_cli.py:70-101`):
1. Bundled CLI at `_bundled/claude` (empty for editable installs)
2. `shutil.which("claude")` — whatever's in PATH
3. Hardcoded fallbacks: `~/.npm-global/bin`, `/usr/local/bin`, `~/.claude/local/claude`

**Key points:**
- Editable install = no bundled CLI = uses your system `claude`
- PyPI wheel bundles a specific CLI version (takes priority over system)
- Override anytime: `ClaudeAgentOptions(cli_path='/path/to/claude')`
- Minimum version: `2.0.0`

**Implication:** SDK and CLI are loosely coupled. You can update one without affecting the other. Patched CLI installs stay untouched.

---

## max_turns: counts API calls per client.query() invocation (2026-02-21)

`max_turns` limits how many Claude API calls happen within a single `client.query()` invocation — it does **not** limit the number of `client.query()` calls on a live client.

When the limit is hit, Claude Code stops and emits `ResultMessage(subtype='error_max_turns', is_error=False)`. The subprocess stays alive, the session persists, and you can call `client.query()` again immediately.

**What "one turn" means:** Each API round-trip = 1 turn. Tool use + tool result together = 2 turns (model call → tool execution → would-be follow-up model call). So `max_turns=1` allows exactly one model API call, stopping before Claude can process the tool result.

```
max_turns=1, task="create a poem":
  Turn 1: Claude → ls (tool call)             ← model API call #1
  Tool executes, returns result
  Turn 2: Claude would process result → STOP   ← error_max_turns
```

**Implication:** `max_turns=1` is useful for step-through debugging but the natural "pause" primitive is hooks (see below).

---

## PostToolUse hook: true step-through debugger (2026-02-21)

The `PostToolUse` hook fires after every tool execution, before Claude makes its next API call. Claude Code literally waits for the hook to return. This is the right primitive for "pause between steps" — not `max_turns`.

**How it works mechanically:**
- Hook callback runs as its own async task inside the SDK's internal `_tg` (task group)
- `receive_response()` in the main loop sits idle waiting for the next message — that's fine, they're concurrent tasks
- The hook can safely `await anyio.to_thread.run_sync(input)` for blocking user input without touching the event loop

```python
async def post_tool_hook(hook_input, tool_use_id, ctx):
    print(hook_input)  # raw: tool_name, tool_input, tool_response
    choice = await anyio.to_thread.run_sync(
        lambda: input("▶ [Enter] continue  [b] block: ").strip().lower()
    )
    if choice == "b":
        return {"continue_": False, "stopReason": "User blocked"}
    return {"continue_": True}

options = ClaudeAgentOptions(
    hooks={"PostToolUse": [HookMatcher(hooks=[post_tool_hook])]},
    ...
)
```

**hook_input fields (PostToolUse):** `tool_name`, `tool_input` (dict), `tool_response` (dict with `stdout`/`stderr` for Bash), `session_id`, `cwd`, etc.

**SDK keeps stdin open when hooks are registered:** `query.py:584-592` — the `stream_input` coroutine waits for the first `ResultMessage` before closing stdin, so the bidirectional control channel stays alive for hook callbacks.

**Return values:** `{"continue_": True}` to proceed, `{"continue_": False, "stopReason": "..."}` to stop mid-task cleanly. Can also add `additionalContext` via `hookSpecificOutput`.

---

## parent_tool_use_id: subagent lineage marker (2026-02-21)

`parent_tool_use_id` on `AssistantMessage`, `UserMessage`, and `StreamEvent` identifies which tool use spawned the subagent that produced this message.

In a single-agent session it's always `None`. It becomes non-null when Claude uses the **Task tool** (or any agent-spawning tool): the subagent's entire message stream gets tagged with the `id` of the `ToolUseBlock` that created it.

```
AssistantMessage(ToolUseBlock id="toolu_abc", name="Task")  ← parent_tool_use_id=None
  │  [subagent session]
  ├── AssistantMessage(ThinkingBlock...)                     ← parent_tool_use_id="toolu_abc"
  ├── AssistantMessage(ToolUseBlock name="Bash" id="toolu_xyz") ← parent_tool_use_id="toolu_abc"
  ├── UserMessage(ToolResultBlock tool_use_id="toolu_xyz")   ← parent_tool_use_id="toolu_abc"
  └── ResultMessage(subtype='success')                       ← parent_tool_use_id="toolu_abc"
UserMessage(ToolResultBlock tool_use_id="toolu_abc")         ← parent_tool_use_id=None
```

**Use cases:** filter top-level vs nested messages, indent subagent activity, reconstruct the full multi-agent call tree.

---

## Subprocess Lifetime: query() vs ClaudeSDKClient (2026-02-20)

**`query()` (standalone function):** Spawns a **new** Claude Code subprocess per call. Stateless, fire-and-forget.

**`ClaudeSDKClient`:** Spawns **one** subprocess that stays alive for the entire client connection. Multi-turn messages are sent by writing to the running process's stdin — no restarts.

**Why it works:** Claude Code is launched with `--input-format stream-json` (`subprocess_cli.py:331`), which puts it into a persistent stdin-reading mode. Each call to `client.query("...")` writes a `{"type": "user", ...}` JSON message to the live process's stdin.

```python
async with ClaudeSDKClient() as client:    # subprocess starts
    await client.query("What is 2+2?")    # stdin write to running process
    async for msg in client.receive_response(): ...

    await client.query("And 3+3?")        # same process, another stdin write
    async for msg in client.receive_response(): ...
# subprocess terminates here (disconnect)
```

**Implication:** `ClaudeSDKClient` is cheap for follow-up turns — no process startup overhead. The process lifetime is exactly the `async with` block (or `connect()`/`disconnect()` pair).

---
