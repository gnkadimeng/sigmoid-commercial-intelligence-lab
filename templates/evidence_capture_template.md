# Evidence Capture Template

This template turns a completed discovery interview into one or more **evidence records** in
`data/processed/discovery_evidence.csv`. Each record links a piece of evidence to a **claim** and a
**decision**.

> **Rule:** one interview may bear on several claims → create **one evidence record per claim**. Do
> not mark anything as validated. Confidence grades move only when the evidence model computes it from
> multiple, independent, low-bias items.

---

## Mapping: interview → evidence records

For the interview you just logged in `data/raw/discovery_interviews.csv`, ask: *which claims does it
speak to?* For each one, add a row to `data/processed/discovery_evidence.csv`.

| Column | How to fill it |
|---|---|
| `evidence_id` | `EVR-####` — sequential, unique |
| `interview_id` | the `interview_id` this came from |
| `decision_id` | the decision it bears on (`D1`/`D2`/`D3`) |
| `claim_id` | the claim it supports/refutes (from `claim_register.csv`) |
| `source_type` | `interview` (or `survey`, `pilot`, `market_report`, `internal_data`, `experiment`) |
| `source_name` | short human label, e.g. "Discovery call — mid-size audit firm" |
| `date_collected` | ISO date |
| `quality_score` | 0.0–1.0, from the interview's `evidence_quality_score` |
| `bias_risk` | `low` / `medium` / `high` |
| `supports_or_refutes` | `supports` / `refutes` / `mixed` / `neutral` |
| `evidence_summary` | one sentence: what this evidence says about the claim |
| `confidence_impact` | `raises`, `lowers`, or `none` — direction only, not a grade change |
| `notes` | context, caveats, quotes |

## Worked example (illustrative — do not commit as real)

> An interview `INT-0001` with an audit firm strongly citing workflow pain would produce:
>
> `EVR-0001, INT-0001, D1, H-SEG-AUDIT-01, interview, "Discovery call — audit firm", 2026-08-01,
> 0.5, medium, supports, "Partner described manual reconciliation as their #1 time sink.", raises,
> "n=1; corroborate before moving the grade."`

## What happens next

1. Save the row(s) in `data/processed/discovery_evidence.csv`.
2. Run `pytest` — the validators check columns, grades, `supports_or_refutes`, and score ranges.
3. Run `quarto render` — the [Claims & Confidence](../evidence/claims-confidence.qmd) and
   [decision](../decisions/index.qmd) pages recompute from the new evidence.
4. Review whether a claim's real-evidence strength changed. **A grade only moves to B when multiple
   independent, low-bias items converge** — one interview is never enough.
5. If a claim clears its `evidence_needed_for_B`, update the claim's `current_confidence_grade` and the
   decision's `current_status` in the registers.
