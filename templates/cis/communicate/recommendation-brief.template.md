# Recommendation Brief — Template

**CIS basis:** §11 Provenance · §15 Decision Confidence · §13 Presentation
**Job:** Communicate — present a decision to stakeholders (execs, investors, clients, partners) with
confidence and full traceability, without losing explainability.
**How to use:** copy to `briefs/<recommendation-id>-brief.md`. One decision per brief. Keep it to a
page; the depth lives in the linked objects.

---

## Recommendation

> **[State the recommended action in one sentence.]**

| Field | Value |
|---|---|
| Recommendation id | R-___ |
| Answers question | Q-___ — [question] |
| Owner · decision date | [name] · [YYYY-MM-DD] |
| Review date | [YYYY-MM-DD] |
| Status | proposed / adopted / superseded / reversed |

## Confidence (§15)

| Confidence | Basis |
|---|---|
| **[0.00–1.00 or D/C/B/A]** | [why this level — evidence strength, validation passed, what would raise it] |

*Recommendations are never binary. This is the current best decision at this confidence — it will
change as evidence changes.*

## Why — the evidence (§11)

| Evidence | Type | Confidence | Supports? |
|---|---|---|---|
| EV-___ | interview / crm_data / market_report / … | Very High / High / Medium / Low | supports / refutes / mixed |
| EV-___ |  |  |  |

**Convergence:** [Do the independent sources agree? Where do they conflict?]

## How — the reasoning (§11 provenance)

| Layer | Object | Note |
|---|---|---|
| Framework | [id] | [logic used] |
| Model | [id] | [what it computed + validation status] |
| Dataset | [id] | [inputs] |

## What we are NOT concluding

- [State the limits — what this brief does *not* claim, so it isn't over-read.]

## Assumptions still open

- [Assumption 1 — how it could be wrong]
- [Assumption 2]

## Next

- [The next experiment or evidence that would raise confidence, or the review trigger.]

---

*Provenance chain: Recommendation → Framework → Model → Dataset → Evidence → Source. Full detail in the
linked object files.*
