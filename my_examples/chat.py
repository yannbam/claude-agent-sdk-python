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
- PostToolUse step-through hook: pause after each tool use
- effort=high + adaptive thinking (ThinkingBlock output shown)
"""
import json
import shutil
from pathlib import Path
from typing import Any

import anyio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    HookContext,
    HookJSONOutput,
    HookMatcher,
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
        "penguinModeOrgEnabled": True
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


GREEN = "\033[32m"
RESET = "\033[0m"


async def post_tool_hook(hook_input: Any, tool_use_id: str | None, ctx: HookContext) -> HookJSONOutput:
    """Pause after each tool use — step-through debugger."""
    print(hook_input)

    # Block here until user decides — runs in a thread so event loop stays free
    choice = await anyio.to_thread.run_sync(
        lambda: input("▶ [Enter] continue  [b] block: ").strip().lower()
    )

    if choice == "b":
        return {"continue_": False, "stopReason": "User blocked this step"}
    return {"continue_": True}


async def main() -> None:
    isolated_home = init_isolated_home()

    options = ClaudeAgentOptions(
        tools=["Bash", "Read", "Write", "Edit"],
        permission_mode="bypassPermissions",
        model="claude-sonnet-4-6",
        effort="high",
        thinking={"type": "adaptive"},    # produces ThinkingBlocks
        # No max_turns — PostToolUse hook handles step-through pausing
        hooks={
            "PostToolUse": [HookMatcher(hooks=[post_tool_hook])]
        },
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
                print(msg)
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, ThinkingBlock):
                            print(f"{GREEN}[thinking] {block.thinking}{RESET}")
                        elif isinstance(block, TextBlock):
                            print(f"{GREEN}{block.text}{RESET}")
            print()

    print("Bye!")


anyio.run(main)
