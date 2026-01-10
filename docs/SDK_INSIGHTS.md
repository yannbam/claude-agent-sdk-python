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
