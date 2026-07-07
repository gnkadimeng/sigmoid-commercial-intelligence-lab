# First Evidence Sprint

**Status:** Planned · v0.1
**Owner:** Commercial Intelligence Lab
**Instruments:** `templates/discovery_interview_script.md`,
`templates/discovery_interview_scoring_guide.md`, `templates/positioning_message_test.md`,
`templates/evidence_capture_template.md`

> **Canonical location:** the in-browser operating page **`start-here/first-evidence-sprint.qmd`**
> (Start Here → First Evidence Sprint on the site) is the source of truth for running the sprint. This
> repo document is a reference copy; when the two differ, prefer the site page and update this file to
> match, to avoid content drift.

This is the plan for the **first real evidence sprint** — the moment the lab stops running on synthetic
data and starts collecting real discovery evidence. It changes no scoring model, no dashboards, and no
confidence grades. It only collects evidence.

---

## Sprint goal

Replace the "no real evidence yet" state on the **Decision 1 (Market Entry)** and
**Decision 2 (Positioning)** claims with the first set of real, structured discovery evidence — so that
each claim shows genuine field signal instead of a bare hypothesis.

**Explicitly not a goal:** validating any claim, moving any claim to grade A, or committing to a
segment or positioning. This sprint is about *first evidence*, not conclusions.

## Segments

1. **Audit firms**
2. **Professional services firms**

## Target interviews

- **8–10 interviews total**, roughly **5 audit + 4 professional services**.
- Minimum to consider the sprint useful: **≥ 3 per segment** with `evidence_quality_score ≥ 40` and
  `bias_risk ≤ 66` (i.e. at least moderate quality, at most medium bias).
- Rotate the positioning-test order across interviews to limit order bias.

## Claims being tested

| Claim | Decision | Question it tests |
|---|---|---|
| **H-SEG-AUDIT-01** | D1 | Do audit firms have strong, specific workflow pain? |
| **H-SEG-AUDIT-02** | D1 | Do audit firms have budget + a buyer for CRM/workflow tools? |
| **H-SEG-PROF-01** | D1 | Do professional-services firms need better pipeline visibility? |
| **H-POS-CRM-01** | D2 | Is "CRM" clear but too generic? |
| **H-POS-REVOPS-01** | D2 | Does "Revenue Operations Platform" express value better? |
| **H-POS-AI-01** | D2 | Is "AI Readiness Platform" differentiated but overpromising? |
| **H-AI-READY-01** | D2 | Do target customers lack structured data? |
| **H-AI-READY-02** | D2 | Would CRM implementation improve AI readiness? |

(D3 / H-GTM-GATE-01 is *observed* via `sales_cycle_signal` and follow-up permission, but is not a
primary target this sprint.)

## Minimum evidence required (per claim)

This sprint aims for **first signal**, not grade changes. As a guide for interpreting results:

- **First real signal:** ≥ 1 direct, first-hand interview record mapped to the claim.
- **Toward grade C (indicative, real):** ≥ 2 independent interviews pointing the same way, quality
  ≥ 40, bias ≤ 66.
- **Toward grade B (substantiated) — usually beyond one sprint:** the claim's `evidence_needed_for_B`
  bar in `data/sample/claim_register.csv` is met by multiple independent, low-bias items *and* is
  reviewed deliberately.

Do not change a grade inside this sprint unless a claim's `evidence_needed_for_B` is genuinely met and
the change is recorded (see "What not to conclude yet").

## How to enter data

1. Run each interview with `templates/discovery_interview_script.md`.
2. Score it the same day with `templates/discovery_interview_scoring_guide.md` (all signal scores
   0–100).
3. Add **one row per interview** to `data/raw/discovery_interviews.csv`, filling every covered field:
   `interview_id, date, company_segment, company_size, respondent_role, decision_linked, claim_linked,
   pain_score, budget_signal, urgency_signal, current_tooling, crm_maturity, workflow_maturity,
   ai_readiness_maturity, positioning_preference, willingness_to_pay_signal, sales_cycle_signal, notes,
   evidence_quality_score, bias_risk, supports_or_refutes`.
   Leave a field blank if it was not covered — **do not fabricate it**.

## How to map interviews into evidence records

Using `templates/evidence_capture_template.md`, for each claim an interview bears on, add **one row**
to `data/processed/discovery_evidence.csv`:
`evidence_id, interview_id, decision_id, claim_id, source_type, source_name, date_collected,
quality_score, bias_risk, supports_or_refutes, evidence_summary, confidence_impact, notes`.

Apply the conversions from the scoring guide:

- `quality_score` = interview `evidence_quality_score` ÷ 100 (→ 0.0–1.0)
- `bias_risk` = band of interview `bias_risk` (0–33 `low`, 34–66 `medium`, 67–100 `high`)
- `source_type` = `interview`
- `confidence_impact` = `raises` / `lowers` / `none` (direction only — never a grade)

## How to run pytest and quarto render

```bash
source .venv/bin/activate
pytest            # validators check columns, grades (A–D), supports/refutes, and score ranges
quarto render     # decision + Claims & Confidence pages recompute from the new records
```

Both must pass before you trust anything. A red suite is a hard stop.

## How to review results

1. **Evidence → Claims & Confidence** — each tested claim now shows a real-evidence count and
   supports/refutes split (instead of "none yet").
2. **Decisions → Market Entry / Positioning** — the claim cards reflect the new evidence.
3. **Start Here → Current Status** — the top-level read of where the decisions stand.
4. Ask, per claim: did independent interviews *converge*? Or does the signal conflict?

## What not to conclude yet

- **Do not** declare a first-target segment or a positioning. A handful of interviews is grade-C signal
  at best.
- **Do not** move a claim to grade A (validated) — that needs a pilot with measured impact.
- **Do not** treat a stated positioning preference as a won deal.
- **Do not** let an enthusiastic-but-biased interview (warm intro, invested respondent) carry a claim —
  that is exactly what `bias_risk` is for.
- If you *do* change a grade because a `evidence_needed_for_B` bar was genuinely met, record the change
  and its rationale (a note or an ADR). Grade changes are decisions, not edits.

---

*This sprint produces evidence, not verdicts. The lab stays at v0.1 hypothesis stage until the evidence
earns otherwise.*
