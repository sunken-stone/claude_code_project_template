Capture or recall reminders via Jarvis. Reminders live in `planning/PLAN.md` Open Reminders and surface automatically before code-write or ExitPlanMode events.

## Two modes

### Mode 1 — Capture (with args)

User invokes: `/remindme <reminder text>` — optionally with explicit Surface hint like "before deploying" or "before exit plan mode"

Jarvis appends the reminder to `planning/PLAN.md` Open Reminders with:
- Next `R-NNN` ID (monotonic)
- Verbatim reminder text
- Inferred Surface trigger:
  - Mentions "before deploy", "before merge", "before exit plan mode" → `before-exit-planning`
  - Mentions "before building", "before writing code", "before implementation" → `before-build`
  - Otherwise → `manual-only`
- Status: `OPEN`

Returns a status line: `✅ planning/PLAN.md — captured R-NNN (Surface: <value>)`

### Mode 2 — Recall (no args)

User invokes: `/remindme` (no arguments)

Jarvis reads `planning/PLAN.md` Open Reminders and returns ALL open reminders grouped by Surface trigger:

```
🎩 OPEN REMINDERS

before-exit-planning:
- R-003 (2026-05-26): Add the new LATE_SHIPMENT env var to .env.example before deploying
- R-007 (2026-05-27): Confirm Slack channel ID with ops before exiting plan mode

before-build:
- R-005 (2026-05-26): Re-read the AHR keyword set before coding the classifier

manual-only:
- R-001 (2026-05-26): Push template repo changes to GitHub

(no OPEN reminders means Jarvis returns: ⏭️ planning/PLAN.md — no open reminders)
```

This is the only Jarvis output that returns the actual content (not a status line) — the user needs to read the reminders.

## Automatic surfacing (main Claude's job)

In addition to manual recall via `/remindme`, **main Claude is responsible for surfacing reminders automatically**:

- **Before calling `ExitPlanMode`:** main Claude reads PLAN.md Open Reminders and surfaces any with `Surface: before-exit-planning` for user review. If any are found, main Claude pauses and asks "These reminders are open before we exit plan mode: <list>. Proceed?"
- **Before any non-trivial code write:** main Claude reads Open Reminders and surfaces any with `Surface: before-build`. Same pause-and-ask flow.

This is codified in `CLAUDE.md` under the Jarvis pre-authorization section. Jarvis itself does not surface mid-conversation — that's main Claude's responsibility.

## Resolution

When a reminder is acted on, Jarvis flips status to `RESOLVED YYYY-MM-DD`. Reminders are NEVER deleted from PLAN.md.

User can manually mark a reminder resolved by saying: "mark R-NNN resolved" — main Claude invokes Jarvis with that instruction.

## How to invoke

Use the Agent tool with `subagent_type: "jarvis"`. Prompt structure:

**Capture mode:**
```
Trigger: /remindme (capture)
Args: <user's reminder text verbatim>

Context (for Surface-trigger inference):
<brief summary of why the reminder was captured — what's happening in the session>

Capture this reminder into planning/PLAN.md Open Reminders and return the status line.
```

**Recall mode:**
```
Trigger: /remindme (recall, no args)

Read planning/PLAN.md Open Reminders and return all OPEN reminders grouped by Surface trigger.
```

## Notes

- Reminders are append-only — never deleted, only flipped to RESOLVED
- Recall mode bypasses the normal silent status-line contract because the user explicitly asked to see the reminders
- Surface trigger inference happens at capture time; user can override by saying e.g. "/remindme R-007 should be Surface: before-build" and Jarvis will update
- Reminders with `Surface: manual-only` only ever surface via `/remindme` recall — they don't auto-fire on ExitPlanMode or code writes
