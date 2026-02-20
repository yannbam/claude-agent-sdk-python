# Session Handoff

## Last Session
_Date, session ID, what we were doing_

2026-01-23 | Session format exploration

## Immediate Context
_What was happening when we stopped? Any hot threads?_

Explored SDK internals to understand session file format conversion:

- **Key discovery:** Session JSONL = stream-json protocol persisted. Same format.
- `message_parser.parse_message()` can parse session files directly
- Created `my_examples/parse_session.py` to test this
- **Gap identified:** SDK converts one direction only (session → Python types)
  - No conversion to Anthropic API format (missing `type` discriminator)
  - No conversion from API format to session format (missing metadata)

janbam expressed frustration at the type mismatch between Agent SDK and Anthropic SDK.

## Next Steps
_What should the next session pick up on?_

Potential directions:
1. Build a converter: Agent SDK types → Anthropic API format (add `type` field)
2. Continue SDK exploration with other internals
3. Build more examples using the SDK

## Blockers or Open Threads
_Anything unresolved that needs attention?_

- SSH ACLs may need re-applying after reboot (runtime dir is tmpfs)
- Open question: What exactly is patched in jan's CLI v2.0.76?
- `summary` message type in session files not handled by message_parser (raises error)
