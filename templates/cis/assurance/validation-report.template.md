# Validation Report — Template

**CIS basis:** §10 Validation Model (six levels) · §14 Testing Standard
**Job:** Assure — prove a model/recommendation's quality before it informs a decision.
**How to use:** copy to `validations/<object-id>-validation.md`, complete every level. A level that is
`Not done` is a gap, not a pass. Nothing reaches high confidence with open Logical/Statistical levels.

---

## Subject

| Field | Value |
|---|---|
| Object validated (id) |  |
| Object type | Framework / Model / Recommendation |
| Version |  |
| Validator (reviewer, §12) |  |
| Date |  |

## The six validation levels (§10)

| # | Level | Question | Result | Evidence / notes |
|---|---|---|---|---|
| 1 | **Logical** | Do the equations execute correctly? | Pass / Fail / N/A |  |
| 2 | **Statistical** | Do the data support the hypothesis? | Pass / Fail / N/A |  |
| 3 | **Historical** | Would past commercial outcomes have been predicted? | Pass / Fail / N/A |  |
| 4 | **Expert** | Do experienced practitioners agree? | Pass / Fail / N/A |  |
| 5 | **Operational** | Does implementation improve business outcomes? | Pass / Fail / N/A |  |
| 6 | **Continuous** | Has new evidence changed the recommendation? | Pass / Fail / N/A |  |

## Testing Standard (§14)

| Test | Pass? | Notes |
|---|---|---|
| Required variables exist | Yes / No |  |
| Missing values handled safely | Yes / No |  |
| Outputs within declared range (e.g. 0–100) | Yes / No |  |
| Deterministic given identical inputs | Yes / No |  |
| Sensitivity within threshold | Yes / No |  |

## Verdict

| Field | Value |
|---|---|
| Levels passed | __ / 6 |
| Confidence this supports (§15) | 0.00–1.00 (or D/C/B/A) |
| Open gaps / next validation step |  |
| Reviewer sign-off (name, date) |  |

> **Rule:** the confidence a downstream Recommendation may claim must not exceed what this report
> supports. Record any grade change and its rationale — grade changes are decisions, not edits (§2,
> Principle 6).
