Signal to Jarvis that the user wants it tuned in to the current planning session. Invokes Jarvis with the planning-mode flag.

## What this does

Launches the Jarvis sub-agent (defined in `.claude/agents/jarvis.md`) via the Agent tool with the explicit planning-mode flag. This is the **manual** trigger path — equivalent to main Claude auto-detecting planning-style discussion, but user-initiated.

Jarvis will:

1. Update `.claude/jarvis_ledger.json` `current_planning_session_id` to mark a new planning session
2. Announce itself with `🤖 Jarvis is tuned in and keeping track.`
3. Read the current state of `memory.md`, `next_steps.md`, `planning/PLAN.md`, `planning/changelog.md`, `planning/explanation.md`
4. Stand ready to capture decisions, reminders, and open questions as they're agreed in this planning session
5. Return status lines (or just the "tuned in" line if no immediate work to do)

## How to invoke

Use the Agent tool with `subagent_type: "jarvis"`. In the prompt, pass:

```
Trigger: /hey jarvis (manual)
Mode: planning

User has explicitly signaled this is a planning session. Tune in, announce, and prepare to capture decisions/reminders/questions as we go.

Current session context summary:
- <2-3 bullet points of what we've been discussing>
- <any decisions already reached but not yet logged>
```

## When to use

- User says "let's plan", "we're brainstorming", "design discussion", or similar
- Before a multi-turn architecture/design conversation begins
- When the user wants Jarvis present from the start of a planning session rather than catching up at the end
- When main Claude's auto-detection didn't fire and the user wants Jarvis tuned in anyway

## What happens during the planning session after Jarvis is tuned in

- Main Claude invokes Jarvis again whenever a clear decision/reminder/question event occurs
- Subsequent invocations are silent (just status lines) — only the first invocation in a planning session announces
- Jarvis tracks the planning session via `.claude/jarvis_ledger.json` until it goes stale (>4h since last invocation) or is explicitly closed via `/memory-update`

## Notes

- Jarvis cannot see the main conversation — the prompt MUST summarize the relevant context
- This command does not write to any project files itself — only invokes Jarvis, which decides what (if anything) to write
- If Jarvis was already tuned in to a planning session (per the ledger), it will skip the announcement and just confirm tune-in is still active
