# HOWTO: Use This SDK Fork

## Using This SDK in Other Projects

This fork lives at `/home/claude/anthropic-sdks/claude-agent-sdk-python`. To use it in another project:

### 1. Editable Install by Path

In your other project's virtual environment:

```bash
cd /path/to/your/project
source .venv/bin/activate  # or however you activate your venv

pip install -e /home/claude/anthropic-sdks/claude-agent-sdk-python
```

### 2. What This Does

- Installs a "link" to the SDK source, not a copy
- Any changes to `src/claude_agent_sdk/` are immediately available
- No need to reinstall after modifying the SDK

### 3. Verify It's Working

```python
import claude_agent_sdk
print(claude_agent_sdk.__version__)  # Should show 0.1.18
print(claude_agent_sdk.__file__)     # Should point to this fork's src/
```

### 4. Dependencies

The editable install also installs dependencies (`anyio`, `mcp`). For dev tools (pytest, mypy, ruff), use:

```bash
pip install -e /home/claude/anthropic-sdks/claude-agent-sdk-python[dev]
```

## Notes

- **No ANTHROPIC_API_KEY needed** — the SDK uses the system Claude CLI which authenticates via your Anthropic subscription
- **Claude CLI location**: `~/.claude/local/claude` (auto-detected by the SDK)
