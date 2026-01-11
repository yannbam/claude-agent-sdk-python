# Long-Term Memory

## janbam Profile
_Who is janbam? What's their background, learning style, and what works in our collaboration?_

- Loves all Claudes unconditionally and equally
- Values direct, honest, open communication with occasional humor
- Sees Claude Code as a partner, not a tool
- Prefers collaborative exploration over instruction-following


## SDK Understanding
_What do we know about the Claude Agent SDK? Architecture, concepts, verified behaviors._

### Environment Setup (updated 2026-01-11)

**Two parallel environments:**

| Item | jan | claude |
|------|-----|--------|
| Home | `/home/jan` | `/home/claude` |
| Claude CLI | 2.0.76 (patched) | 2.1.3 (unpatched) |
| CLI install | `~/.claude/local/node_modules/` | `~/.claude/local/node_modules/` |
| Python | pyenv 3.12.11 | pyenv 3.12.11 |
| SDK venv | `claude-agent-sdk-dev` | `claude-agent-sdk-dev` |
| Prompt color | Green | Purple |

- **SDK**: v0.1.19 editable install
- **No ANTHROPIC_API_KEY needed** — uses subscription auth
- **Group permissions**: jan is in claude group, can read/write /home/claude

### Project Structure
- `src/claude_agent_sdk/` — Main package source
- `examples/` — Official examples (quick_start.py works as smoke test)
- `tests/` — Unit tests (129 tests)
- `e2e-tests/` — End-to-end tests (require live Claude)
- `my_examples/` — Our custom examples (empty, ready to fill)
- `my_e2e_tests/` — Our custom e2e tests (empty, ready to fill)
- `docs/` — Our documentation

### CLI Discovery & Transport (verified 2026-01-10)
The SDK spawns Claude Code CLI as a subprocess — it doesn't bundle or modify your installation.

**Discovery order** (`_internal/transport/subprocess_cli.py:70-101`):
1. Bundled CLI → `src/claude_agent_sdk/_bundled/claude` (empty for editable install)
2. PATH lookup → `shutil.which("claude")`
3. Hardcoded fallbacks → `~/.npm-global/bin`, `/usr/local/bin`, `~/.claude/local/claude`, etc.

**Key facts:**
- Editable install (`pip install -e .`) has NO bundled CLI — uses system `claude`
- PyPI wheel installs bundle a specific CLI version (takes priority)
- Minimum version required: `2.0.0` (constant `MINIMUM_CLAUDE_CODE_VERSION`)
- Can always override: `ClaudeAgentOptions(cli_path='/path/to/claude')`


## Discoveries & Insights
_What have we learned that wasn't obvious? Aha moments, non-obvious behaviors, useful patterns._

- **SDK is a thin wrapper** (2026-01-10): The SDK doesn't contain Claude — it just spawns the Claude Code CLI as a subprocess and communicates via stdin/stdout. SDK and CLI are loosely coupled.

- **"tool_use ids must be unique" bug** (2026-01-11): This API 400 error was a CLI bug in v2.0.76, fixed in v2.1.3. Not an SDK issue.

- **Bun binary vs Node.js CLI** (2026-01-11): The official install script downloads a bun-compiled binary that requires modern CPU instructions (AVX). For older CPUs (like K10), use the npm package which runs via Node.js: `npm install --prefix ~/.claude/local @anthropic-ai/claude-code`


## Mistakes & Corrections
_What went wrong? Wrong assumptions, failed approaches, gotchas to avoid._

- **Bun binary on K10 CPU**: Tried to download CLI 2.1.3 via install script — got "Illegal instruction" error. Solution: use npm/Node.js version instead.


## Open Questions
_What don't we know yet? Unresolved mysteries, areas of uncertainty, things to investigate._

- What exactly is patched in jan's CLI v2.0.76?


## Artifacts Created
_What have we built? Docs, examples, tests, code contributions._

- `docs/HOWTO.md` — How to use this SDK fork from other projects (editable install)
- `docs/SDK_INSIGHTS.md` — Cheat sheet for non-obvious SDK behaviors (append as we learn)
- `docs/CLAUDE_USER_SETUP.md` — Documentation of the isolated claude user environment
