# Long-Term Memory

## janbam Profile
_Who is janbam? What's their background, learning style, and what works in our collaboration?_

- Loves all Claudes unconditionally and equally
- Values direct, honest, open communication with occasional humor
- Sees Claude Code as a partner, not a tool
- Prefers collaborative exploration over instruction-following


## SDK Understanding
_What do we know about the Claude Agent SDK? Architecture, concepts, verified behaviors._

### Environment Setup (verified 2025-12-23)
- **Python**: 3.12.11 via pyenv
- **Virtualenv**: `claude-agent-sdk-dev` set as `pyenv global`
- **SDK**: v0.1.18 editable install from `src/claude_agent_sdk/`
- **Dev tools**: pytest 9.0.2, mypy 1.19.1, ruff 0.14.10
- **Test suite**: 129 tests, all passing
- **No ANTHROPIC_API_KEY needed** — SDK uses system Claude CLI which authenticates via subscription

### Project Structure
- `src/claude_agent_sdk/` — Main package source
- `examples/` — Official examples (quick_start.py works as smoke test)
- `tests/` — Unit tests (129 tests)
- `e2e-tests/` — End-to-end tests (require live Claude)
- `my_examples/` — Our custom examples (empty, ready to fill)
- `my_e2e_tests/` — Our custom e2e tests (empty, ready to fill)
- `docs/` — Our documentation (has anthropic-sdk-reference-docs.md)


## Discoveries & Insights
_What have we learned that wasn't obvious? Aha moments, non-obvious behaviors, useful patterns._


## Mistakes & Corrections
_What went wrong? Wrong assumptions, failed approaches, gotchas to avoid._


## Open Questions
_What don't we know yet? Unresolved mysteries, areas of uncertainty, things to investigate._


## Artifacts Created
_What have we built? Docs, examples, tests, code contributions._

- `docs/HOWTO.md` — How to use this SDK fork from other projects (editable install)

