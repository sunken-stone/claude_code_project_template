# claude_skills_list.md — Slash Commands Reference

Single source of truth for all slash commands and skills available in this project. Maintained by Jarvis whenever a new skill is added.

Skills live in `.claude/commands/<name>.md` (slash commands) or `.claude/skills/<name>/SKILL.md` (skill-format). Invoke any with `/<skill-name>`.

---

## Session Management

| Skill | Path | Description | When to use |
|---|---|---|---|
| `/hey-jarvis` | `.claude/commands/hey-jarvis.md` | Signal that this is a planning session — tunes Jarvis in | Start of design / architecture / scope discussion |
| `/remindme` | `.claude/commands/remindme.md` | Capture (with args) or recall (no args) reminders | Anytime you want to defer a thought to a specific moment (`before-build`, `before-exit-planning`, or `manual-only`) |
| `/memory-update` | `.claude/skills/memory-update/SKILL.md` | End-of-session orchestrator — batches all doc updates through Jarvis | When wrapping up a session |

---

## Jarvis Sub-Agent

| Agent | Path | Description |
|---|---|---|
| `jarvis` | `.claude/agents/jarvis.md` | Record-keeping sub-agent — Memory Keeper + Decision Tracker + Documentation Keeper + PM |

---

## Project-Specific Skills

_(Add project skills here as they're created. Format: name, path, description, when-to-use.)_
