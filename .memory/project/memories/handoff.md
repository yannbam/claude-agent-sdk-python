# Session Handoff

## Last Session
_Date, session ID, what we were doing_

2026-01-11 | Session f5b47d84 | Setup claude user environment + fix tool_use bug

## Immediate Context
_What was happening when we stopped? Any hot threads?_

Fixed "tool_use ids must be unique" error by setting up isolated claude user with CLI 2.1.3:
- Created `/home/claude` user with group permissions (jan in claude group)
- Installed Claude Code 2.1.3 via npm (Node.js version, not bun binary)
- Set up pyenv + virtualenv `claude-agent-sdk-dev`
- Updated SDK to v0.1.19
- `quick_start.py` now works!

## Next Steps
_What should the next session pick up on?_

Ready for actual SDK exploration:
1. Read through main SDK entry points (`query.py`, `client.py`)
2. Run and study the official examples
3. Start building our own examples in `my_examples/`

## Blockers or Open Threads
_Anything unresolved that needs attention?_

- MCP memory tools may not work when running as claude user (different config)
- Open question: What exactly is patched in jan's CLI v2.0.76?
