#!/usr/bin/env python3
"""
Minimal interactive multi-turn chat with Claude.

Completely isolated settings environment:
- Stable HOME at ~/tmp/claude-chat/ (created once, persists across runs)
- OAuth credentials copied from ~/.claude/.credentials.json
- Minimal ~/.claude.json with only auth fields + our settings
- No user settings loaded (setting_sources=None default)
- autoCompactEnabled: false, autoUpdates: false, installMethod: local
- CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
- No tools, no system prompt
- effort=high + adaptive thinking (ThinkingBlock output shown)
"""
import json
import shutil
from pathlib import Path

import anyio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
    ThinkingBlock,
)

# Stable isolated HOME — persists across runs, safe to tweak manually
ISOLATED_HOME = Path.home() / "tmp" / "claude-chat"

# Auth fields to copy from the real ~/.claude.json
AUTH_KEYS = ("oauthAccount", "userID", "anonymousId")


def init_isolated_home() -> Path:
    """Initialize isolated HOME once. Skip entirely if it already exists."""
    if ISOLATED_HOME.exists():
        return ISOLATED_HOME

    print(f"Initializing isolated HOME at {ISOLATED_HOME} ...")
    ISOLATED_HOME.mkdir(parents=True)

    # Write .claude.json: our settings + auth fields from real ~/.claude.json
    real_claude_json = Path.home() / ".claude.json"
    isolated_data: dict = {
        "autoCompactEnabled": False,
        "installMethod": "local",
        "autoUpdates": False,
    }
    if real_claude_json.exists():
        data = json.loads(real_claude_json.read_text())
        for key in AUTH_KEYS:
            if key in data:
                isolated_data[key] = data[key]

    (ISOLATED_HOME / ".claude.json").write_text(json.dumps(isolated_data, indent=2))

    # Copy .credentials.json (actual OAuth tokens)
    src_creds = Path.home() / ".claude" / ".credentials.json"
    if src_creds.exists():
        dest_claude_dir = ISOLATED_HOME / ".claude"
        dest_claude_dir.mkdir(exist_ok=True)
        dest_creds = dest_claude_dir / ".credentials.json"
        shutil.copy2(src_creds, dest_creds)
        dest_creds.chmod(0o600)
        print("Copied .credentials.json")
    else:
        print("Warning: ~/.claude/.credentials.json not found — may need to /login")

    return ISOLATED_HOME


async def main() -> None:
    isolated_home = init_isolated_home()

    options = ClaudeAgentOptions(
        allowed_tools=[],                 # no tools
        model="claude-sonnet-4-6",
        effort="high",
        thinking={"type": "adaptive"},    # produces ThinkingBlocks
        env={
            "HOME": str(isolated_home),
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
        },
    )

    async with ClaudeSDKClient(options) as client:
        await client.connect()
        print("Claude is ready. Type 'quit' or Ctrl+C to exit.\n")

        while True:
            # Run blocking input() in a thread so the event loop stays alive
            try:
                user_input = await anyio.to_thread.run_sync(
                    lambda: input("You: ")
                )
            except (EOFError, KeyboardInterrupt):
                break

            if user_input.strip().lower() in ("quit", "exit", "q"):
                break
            if not user_input.strip():
                continue

            await client.query(user_input)

            # Collect response until ResultMessage
            async for msg in client.receive_response():
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, ThinkingBlock):
                            print(f"\n[thinking]\n{block.thinking}\n[/thinking]\n")
                        elif isinstance(block, TextBlock):
                            print(f"Claude: {block.text}")
            print()

    print("Bye!")


anyio.run(main)
