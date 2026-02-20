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
