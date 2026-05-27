# PLAN.md — [Project Name]

Build, feature, and decision plan for this project. Three Jarvis-owned sections live in this file (Decisions Ledger, Open Reminders, Open Questions) — see `.claude/agents/jarvis.md` for the contract.

For project-level scope confirmation, see `PROJECT_SCOPE.md` (root).
For deploy/execution steps, see `planning/execution.md`.
For plan-change history, see `planning/changelog.md`.

---

## Plan Changelog

Reverse-chronological table of plan changes. Ship events are not listed here — they live in `memory.md`. Plan changes only. Full detail for each entry lives in `planning/changelog.md`.

This table is maintained automatically by the `/memory-update` skill via Jarvis.

| Date | Change |
|---|---|
| _(no plan changes recorded yet)_ | _ |

---

## Current Plan / Scope Summary

_(Living section — what we're building right now. Updated whenever scope or approach changes materially.)_

---

## Decisions Ledger

Jarvis-owned. Verbatim capture of decisions reached during planning conversations. Append-only — entries are never deleted, only flipped through lifecycle states (OPEN → BUILT → SUPERSEDED).

### Format

```
### D-NNN — [short title]
**Date:** YYYY-MM-DD
**Source:** session N | /hey jarvis | /remindme | EnterPlanMode | mid-session detection
**Decision:** [verbatim agreed outcome — quote the conversation]
**Reasoning:** [verbatim from conversation]
**Constraints:** [verbatim, if any]
**Status:** OPEN
**Built-because:** _(populated when status flips to BUILT)_
```

### Lifecycle

- **OPEN** → decision agreed, not yet built
- **BUILT YYYY-MM-DD** → decision implemented in code; `Built-because:` populated with one-line reason; corresponding entry added to `planning/changelog.md`
- **SUPERSEDED → D-NNN** → approach revised; original text preserved verbatim; inline supersession callout added immediately below

---

## Open Reminders

Jarvis-owned. Captured via `/remindme <text>` or main Claude during decision moments. Append-only — flipped to RESOLVED, never deleted.

### Format

```
### R-NNN — [reminder text]
**Captured:** YYYY-MM-DD
**Surface:** before-build | before-exit-planning | manual-only
**Status:** OPEN
```

### Surface trigger semantics

- **`before-build`** — main Claude surfaces before any non-trivial code write
- **`before-exit-planning`** — main Claude surfaces before calling `ExitPlanMode`
- **`manual-only`** — only surfaces when user invokes `/remindme` recall

### Current entries

### R-001 — push template repo changes to GitHub
**Captured:** 2026-05-26
**Surface:** manual-only
**Status:** OPEN

---

## Open Questions

Jarvis-owned. Captured when a question surfaces in conversation that can't be answered immediately. Append-only — flipped to ANSWERED with a link to the resolving Decisions Ledger entry, never deleted.

### Format

```
### Q-NNN — [question]
**Surfaced:** YYYY-MM-DD
**Why it matters:** [one line]
**Status:** OPEN | ANSWERED → D-NNN
```

---

## Build Plan

_(Project-specific plan sections continue below. Add Part 1, Part 2, etc. as the project grows.)_
