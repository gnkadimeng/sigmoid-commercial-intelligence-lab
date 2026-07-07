# Discovery Interview Template

Use this template to run a structured discovery interview and capture it as one row in
`data/raw/discovery_interviews.csv`. One completed interview = one row. Keep answers factual; record
what the respondent actually said, not what we hope they said.

> **This does not create validated evidence.** A single interview is a data point. Confidence only
> moves when independent interviews converge — see `templates/evidence_capture_template.md`.

---

## 1. Interview metadata

- **interview_id:** `INT-####` (sequential, unique)
- **date:** ISO date `YYYY-MM-DD`
- **respondent_role:** e.g. Partner, Ops Lead, Finance Director
- **company_segment:** e.g. Audit, Professional Services, Mining Supplier, Municipality
- **company_size:** employee band, e.g. `11-50`, `51-200`, `201-500`, `500+`

## 2. What this interview is about

- **decision_linked:** which decision this bears on — `D1`, `D2`, or `D3`
- **claim_linked:** which claim(s) this bears on — e.g. `H-SEG-AUDIT-01`
  (use the ids in `data/sample/claim_register.csv`)

## 3. Signals (score 0–100 unless noted)

| Field | Prompt | Capture |
|---|---|---|
| `pain_score` | How acute and specific is the workflow pain? | 0 = none, 100 = severe, funded, urgent |
| `budget_signal` | Is there a real budget line and a buyer? | 0 = none, 100 = active budget + buyer |
| `urgency_signal` | Is there a compelling event / timeline? | 0 = none, 100 = must-solve-now |
| `willingness_to_pay_signal` | Any concrete price reaction? | 0 = none, 100 = clear WTP at target price |
| `sales_cycle_signal` | Expected time to close | 0 = very long, 100 = very short |
| `crm_maturity` | Current CRM sophistication | 0–100 |
| `workflow_maturity` | How defined are their workflows? | 0–100 |
| `ai_readiness_maturity` | Data structure / analytics practice | 0–100 |

- **current_tooling:** free text — what they use today
- **positioning_preference:** `CRM`, `RevOps`, `AI Readiness`, or `unclear`

## 4. Evidence quality (be honest)

- **evidence_quality_score:** 0.0–1.0 — rigour, directness, recency of this single source.
  A one-off call is rarely above ~0.5.
- **bias_risk:** `low` / `medium` / `high` — did we lead the witness? Is the respondent
  incentivised to please us? Selection bias in who we spoke to?
- **supports_or_refutes:** does this interview `supports`, `refutes`, `mixed`, or `neutral` on the
  linked claim?

## 5. Notes

- **notes:** verbatim quotes and context. Prefer the respondent's own words over paraphrase.

---

## After the interview

1. Add the row to `data/raw/discovery_interviews.csv`.
2. Turn it into evidence records using `templates/evidence_capture_template.md`.
3. Run `pytest` and `quarto render`; check whether any claim's confidence changed.
