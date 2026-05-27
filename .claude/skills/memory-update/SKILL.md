---
name: memory-update
description: Use this skill at the end of a Claude Code session to log what was accomplished into memory.md and sync drift across all planning docs. Triggers when the user says "we're done", "end of session", "wrap up", "save our progress", "update memory", "log what we did", "session complete", "I'm done for today", "let's close out", "write up the session", "record what we built", "before we go", "that's it for today", "update memory.md", "save context", "commit and close", "done for the day", "calling it", "signing off", "finished for today", "all done", "shutting down", "logging off", "that's a wrap", or any indication the current work session is ending. Does not trigger mid-session when the user is still actively building.
allowed-tools: Read Edit Write Agent
metadata:
  model: claude-sonnet-4-6
---

# memory-update — End-of-Session Orchestrator

This skill is a thin orchestrator. It **detects** what changed during the session, then **delegates** every file write to the **Jarvis subagent** (`.claude/agents/jarvis.md`) via a batch invocation. Jarvis owns the detailed file-by-file formatting rules — this skill only decides which files need updating and hands them off.

## Files in scope

For each file, decide whether this session produced a change that warrants an update. If yes, include it in the batch brief to Jarvis.

1. **`memory.md`** — always update (every session gets a log entry)
2. **`planning/PLAN.md`** — update if any decisions were reached, reminders captured, or open questions surfaced
3. **`planning/changelog.md`** — update if any decisions were BUILT or a true plan change occurred
4. **`planning/explanation.md`** — update if any data/concept clarifications surfaced
5. **`planning/raid.md`** — update if any risks, assumptions, issues, or RAID-level decisions surfaced
6. **`planning/cost_log.md`** — update if engineering hours, API spend, or other cost signals came up
7. **`next_steps.md`** — update with any unfinished items + unresolved Open Reminders/Questions
8. **`README.md`** — update only if user-facing behavior, architecture, or required env vars changed
9. **`claude_skills_list.md`** — update if a new skill was created or an existing one materially changed

## Plan-change detection

The canonical definition of a "plan change" lives in `.claude/agents/jarvis.md` under the **Three-part plan-change protocol** section. Do not duplicate it here. When uncertain whether something is a plan change, delegate to Jarvis and let it enforce the gate on its side.

## Delegation pattern — batch invocation REQUIRED

Use **one Jarvis call** with a batch brief. The shape:

```
Trigger: /memory-update (end-of-session sweep)

Files to update:
1. memory.md — <one-line summary of what to log>
2. planning/PLAN.md — <one-line summary>
3. README.md — <one-line summary>
... (only files that actually need updating)

Shared session context (applies to all of the above):
<self-contained narrative summary of session events — Jarvis cannot see parent conversation>

Git ground truth (run `git status --porcelain && git diff --stat HEAD` before briefing):
<paste the output here so Jarvis has authoritative file-change list, not just narrative>

Decisions reached this session (for PLAN.md Decisions Ledger):
- <decision 1 — verbatim from conversation>
- <decision 2 — verbatim>

Reminders captured this session (for PLAN.md Open Reminders):
- <reminder 1>

Open questions surfaced this session (for PLAN.md Open Questions):
- <question 1>

Constraints (if any):
- <any special rules for this batch>
```

Jarvis processes the files in order and returns one status line per file. Reading shared state (like the next memory.md session number) happens ONCE and is reused across the batch. This is significantly cheaper than N sequential one-file calls.

Jarvis return line examples:
- `✅ memory.md — appended Session 12 entry`
- `✅ planning/PLAN.md — added D-007, R-003, Q-002`
- `⏭️ README.md — already up-to-date`
- `❓ planning/raid.md — references I-014 but no entry; verify content?`

Collect all status lines and present them as a brief summary to the user.

## After all delegations complete

Surface any `❓` clarifications to the user immediately — these need user input before the session can fully close.

Then remind the user to stage and commit each changed file separately, one commit per file (per CLAUDE.md commit conventions):

```
git add memory.md && git commit -m "docs: update session log"
git add planning/PLAN.md && git commit -m "docs: log decisions/reminders/questions"
git add planning/explanation.md && git commit -m "docs: update explanations"   # only if changed
git add README.md && git commit -m "docs: update README"                        # only if changed
git add planning/raid.md && git commit -m "docs: update RAID"                   # only if changed
git add planning/cost_log.md && git commit -m "docs: update cost log"           # only if changed
git add planning/changelog.md && git commit -m "docs: log plan change — [title]"  # only if plan change
git add next_steps.md && git commit -m "docs: carry forward open items"         # only if changed
```

## Gotchas

- **Always delegate, do not inline-write.** Jarvis owns the formatting rules. Bypassing it splits the source of truth.
- **Brief Jarvis fully.** Jarvis has no access to the parent conversation. Every brief must be self-contained.
- **One batch Jarvis call** — not N sequential calls. Significantly cheaper.
- **Decisions go in PLAN.md Decisions Ledger VERBATIM.** Don't paraphrase them in the brief — quote the conversation.
- **Ship events go in `memory.md` only — never in `planning/changelog.md` unless they involve a plan change.**
- **Session numbers increment from the last entry in `memory.md`** — Jarvis reads the file once to get the count for the whole batch.
- **`/memory-update` clears the planning session in the ledger** — Jarvis sets `current_planning_session_id` back to null so the next `/hey jarvis` invocation starts a fresh announce.
