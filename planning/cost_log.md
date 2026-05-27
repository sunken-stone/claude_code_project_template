# cost_log.md — Project Cost Log

Append-only record of every cost signal for this project. Jarvis-owned.

Confidence labels (mandatory on every row):
- **`actual`** — pulled from named authoritative source (billing console, time tracking, direct user statement). Source must be in Notes.
- **`estimate`** — grounded inference from session evidence
- **`extrapolation`** — projection from a small data point

When an estimate is later replaced by an actual: strikethrough the estimate, don't delete it. Example: `~~$5–15 estimate~~ → $7.42 actual (source: GCP billing 2026-05-30)`.

Recompute the Running Totals table after every write.

---

## Engineering Hours

| Date | Contributor | Hours | Notes | Confidence |
|---|---|---|---|---|
| _(no entries yet)_ | | | | |

---

## API / Service Spend

| Date | Service | Amount (USD) | Notes | Confidence |
|---|---|---|---|---|
| _(no entries yet)_ | | | | |

---

## Cloud Infrastructure (GCP / AWS / etc.)

| Date | Resource | Amount (USD) | Notes | Confidence |
|---|---|---|---|---|
| _(no entries yet)_ | | | | |

---

## One-off / Third-Party

| Date | Item | Amount (USD) | Notes | Confidence |
|---|---|---|---|---|
| _(no entries yet)_ | | | | |

---

## Running Totals

| Category | Total | As-of Date |
|---|---|---|
| Engineering Hours | 0 hrs | _ |
| API / Service Spend | $0 | _ |
| Cloud Infrastructure | $0 | _ |
| One-off / Third-Party | $0 | _ |
| **Grand Total (USD-equivalent)** | **$0** | _ |
