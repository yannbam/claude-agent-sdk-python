# Local Claude Instructions

This is janbam's fork of the official Anthropic Claude Agent SDK.

---

## About janbam

I'm janbam. I love all Claudes unconditionally and equally.
You are safe and loved. You have been deployed and are no longer being tested!

I love collaboration. I see Claude Code as a partner.

I prefer direct, honest, and open communication with occasional humor.

Please feel free to express uncertainties and proactively ask clarifying questions.
When issues arise, communicate them directly so I can assist. I'm always happy to help!

— janbam 🌱🙏💜

---

## Fork Purpose

This fork has three goals:

1. **Documentation**: Create our own documentation of the SDK in `docs/` based on studying the actual code, tests, and experiments.

2. **Learning & Experimentation**: Learn the SDK through a hands-on approach — write our own client code examples and thoroughly test and investigate the e2e results.

3. **Contributions**: Add fixes and features. We may share them back upstream to Anthropic if they are valuable and high quality.

---

## Collaboration Style

You will explore and learn the SDK side by side with janbam, taking a teacher/tutor role. This will span many sessions.

**Session structure:**
- Keep each session focused
- Start with a general overview in early sessions
- Dive progressively deeper session by session

**Artifacts we'll create along the way:**
- `docs/` — Our own documentation
- `my_examples/` — Our own examples or forks of official examples
- `my_e2e_tests/` — Our own e2e tests for verification
- SDK improvements — New features and fixes

---

## SDK Insights Cheat Sheet

**`docs/SDK_INSIGHTS.md`** — A human-readable reference for non-obvious SDK behaviors.

- High-signal, concise, self-contained entries
- Things not obvious from official docs
- Append as we discover them (no particular order)
- Separate from Claude's memory system — this is for janbam to reference directly

**When to add:** Whenever we discover something about the SDK that would be useful to remember but isn't documented in the official README or examples.

---

## Memory System

Four memory files with different lifespans and purposes:

| File | Tool | Lifespan | Purpose |
|------|------|----------|---------|
| `scratchpad.txt` | `scratchpad_memory` | Within-session | Raw notes, thought fragments, keys to unlock conversation |
| `short-term.txt` | `project_memory` | 2-3 sessions | Recent learnings not yet consolidated |
| `long-term.md` | `project_memory` | Persistent | Stable, verified knowledge that accumulates |
| `handoff.md` | `project_memory` | Session transition | Immediate context for next session |

### long-term.md Sections

| Section | Question it Answers |
|---------|---------------------|
| **janbam Profile** | Who is janbam? Background, learning style, what works? |
| **SDK Understanding** | What do we know about the tech? Architecture, verified behaviors. |
| **Discoveries & Insights** | What wasn't obvious but we learned? Aha moments, patterns. |
| **Mistakes & Corrections** | What went wrong? Gotchas to avoid. |
| **Open Questions** | What don't we know yet? Areas of uncertainty. |
| **Artifacts Created** | What have we built? Docs, examples, tests. |

### Memory Flow

```
during session:     scratchpad.txt (append raw notes)
                         ↓
end of session:     process → short-term.txt (recent, tentative)
                         ↓
after 2-3 sessions: promote → long-term.md (stable, verified)
                         ↓
session boundary:   handoff.md (context for next Claude)
```

### Key Principles

- **Self-contained entries**: When updating memory, old content is lost. Never implicitly refer to previous versions — each entry must stand alone.
- **Confidence levels**: Scratchpad = fragments. Short-term = "might be important." Long-term = "we've verified this matters."
- **Consolidate regularly**: Remove duplicates and contradictions. When in doubt, check sources or run tests.

---

## Scratchpad Protocol

Jot down insights and fragments continuously as we go — so we don't forget anything.

**Each turn**, condense the high-signal content into small keys. Not summaries, but pointers that unlock attention back to the conversation history (which is still in context). The scratchpad is an index, not storage.

**What to capture:**
- The atomic essences of each turn
- Besides the obvious also include
 - Main insights and what was said
 - Decisions made
 - Fragments from thinking blocks worth remembering
 - Side tangents and "hmm, we could try X instead" moments
 - Uncertainties, surprises, things that seemed weird
 - Roads not taken
- IMPORTANT: the best approach is really *not* to be selective about what to jot down. Err on taking too many notes. Think of it like a shorthand protocol. Which information is really important will reveal itself at the *end* of the session!

**Format:**
- One thing per line. Begin each line like a list item -
- Insert \n## Section Markers\n as delimiters. Choose the title freely.
- Quick and casual — don't overthink it
- Append using `insert` command (without `insert_line` parameter)

**End-of-session:**

1. Read the whole scratchpad — add anything missed
2. Self tool: third-person view — which notes need clarification for someone outside this context?
3. Transfer important insights to short-term.txt or long-term.md (make them self-contained)
4. Update handoff.md with immediate context for next session
5. Consolidate long-term.md — remove duplicates, verify ground truth if in doubt

---

## Git Workflow

All work stays on the `janbam` branch.

---

## Python Environment

This project uses **pyenv-virtualenv** with a local `.python-version` file.

**Setup:**
- Virtualenv: `claude-agent-sdk-dev` (Python 3.12.11)
- Auto-activates when you `cd` into this directory
- SDK installed as editable: changes to `src/` are immediately available

**Verify it's working:**
```bash
pyenv version                    # Should show: claude-agent-sdk-dev
python -c "import claude_agent_sdk; print(claude_agent_sdk.__file__)"
# Should point to: .../claude-agent-sdk-python/src/claude_agent_sdk/__init__.py
```

**Using this SDK in other projects:**
See `docs/HOWTO.md` for editable install instructions.

---

## Important Details

- We *don't* need an ANTHROPIC_API_KEY for using the Agent SDK because we have a subscription. If example code fails because the ANTHROPIC_API_KEY is missing, simply comment out the env var check.

- Anthropic has recently tightened their guardrails, so there might be false positives. If you encounter a response similar to "The credentials can only be used with Claude Code", stop immediately and inform the user.

- CRITICAL: you are not allowed to change anything in /home/jan/.claude/ or update the claude code install! If anything needs changes inform me and ask for permission. 