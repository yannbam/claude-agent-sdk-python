#!/usr/bin/env python3
"""Parse a Claude Code session JSONL file using the SDK's message_parser.

Usage: python parse_session.py <session.jsonl>
       python parse_session.py <session.jsonl> --raw   # no pretty print
"""

import json
import sys
from dataclasses import fields, is_dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from claude_agent_sdk._internal.message_parser import parse_message


def pp(obj, indent=0):
    """Pretty print a dataclass."""
    pad = "  " * indent
    if is_dataclass(obj):
        name = type(obj).__name__
        lines = [f"{name}("]
        for f in fields(obj):
            val = getattr(obj, f.name)
            if val is None:
                continue
            if isinstance(val, list) and len(val) > 0:
                lines.append(f"{pad}  {f.name}=[")
                for item in val:
                    lines.append(f"{pad}    {pp(item, indent+2)},")
                lines.append(f"{pad}  ]")
            elif isinstance(val, str) and len(val) > 80:
                lines.append(f"{pad}  {f.name}={val[:80]!r}...")
            else:
                lines.append(f"{pad}  {f.name}={val!r}")
        lines.append(f"{pad})")
        return "\n".join(lines)
    return repr(obj)


if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(1)

path = sys.argv[1]
raw_mode = "--raw" in sys.argv

with open(path) as f:
    for i, line in enumerate(f, 1):
        if not line.strip():
            continue
        raw = json.loads(line)
        try:
            msg = parse_message(raw)
            if raw_mode:
                print(f"[{i}] {msg}")
            else:
                print(f"[{i}] {pp(msg)}")
            print()
        except Exception as e:
            print(f"[{i}] ERROR: {e}")
            print()
