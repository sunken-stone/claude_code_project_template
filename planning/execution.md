# execution.md — Deploy & Runbook Steps

Project-specific deployment, secrets-sync, and operational runbook steps. Jarvis-owned.

Add new env vars to both the `gcloud secrets create` step AND the `--set-secrets` / `--update-secrets` step when they're introduced.

Document `.env` parsing caveats that would burn a future contributor (e.g. inline comments, trailing whitespace, quote handling).

---

## Initial Setup

_(One-time setup steps for a new contributor or a fresh deploy environment.)_

---

## Routine Deploy

_(Standard deploy sequence — what runs, in what order, how to verify.)_

---

## Secrets Sync

_(How `.env` values get pushed to the secrets backend. Includes the `--set-secrets` vs. `--update-secrets` distinction if it matters in this project.)_

---

## Runbook — Common Failures

_(What to do when X breaks. Add entries as failures are encountered.)_

---

## Env Var Reference

| Var | Required? | Default | Notes |
|---|---|---|---|
| _(no env vars documented yet)_ | | | |

---

## `.env` Parsing Caveats

_(Project-specific gotchas — e.g. "no inline `#` comments after values" — added as discovered.)_
