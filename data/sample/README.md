# data/sample/

**Synthetic sample data.** Versioned, committed, and used to exercise the scoring, validation, and
evidence machinery and to render the dashboards.

> **These are not real market facts.** All values are invented for demonstration. Nothing here may be
> cited as evidence at v0.1.

## Files

### `market_segments.csv`
One row per candidate market segment. Sub-scores are on a **0–10** scale.

| Column | Meaning |
|---|---|
| `segment_id` | Unique id (e.g. `SEG-01`). |
| `segment_name`, `industry` | Human labels. |
| `market_size_score` | Addressable size (higher = larger). |
| `pain_score` | Acuteness of the problem (higher = more pain). |
| `budget_score` | Ability/willingness to pay. |
| `competition_score` | Competitive intensity (**penalty**: higher = worse). |
| `sales_cycle_score` | Length of sales cycle (**penalty**: higher = longer/worse). |
| `strategic_fit_score` | Fit with Sigmoid's capabilities/narrative. |
| `evidence_quality_score` | How much we actually know about this segment. |

Consumed by `calculate_market_priority_score` and the Market Prioritisation dashboard.

### `customer_profiles.csv`
One row per synthetic customer/company. Maturity/signal columns are **0–10**.

| Column | Meaning |
|---|---|
| `customer_id`, `company_name`, `industry`, `employee_band` | Identity + firmographics. |
| `current_crm_maturity` | Existing CRM sophistication. |
| `workflow_maturity` | How defined their workflows are. |
| `data_quality` | Cleanliness/completeness of their data. |
| `analytics_maturity` | Existing analytics practice. |
| `ai_readiness` | Assessed organisational AI readiness. |
| `budget_signal`, `urgency_signal` | Buying signals. |
| `decision_complexity` | Buying-committee complexity (**penalty** in fit). |

Consumed by `calculate_customer_fit_score` and `calculate_ai_readiness_score`.

### `evidence_register.csv`
One row per evidence item linked to a claim (`claim_id`).

| Column | Meaning |
|---|---|
| `evidence_id` | Unique id. |
| `claim_id` | The hypothesis/recommendation it bears on. |
| `source_type` | `proposal` / `interview` / `survey` / `market_report` / `internal_data` / `experiment` / `public_stat`. |
| `source_name` | Human description of the source. |
| `date_collected` | ISO date. |
| `quality_score` | Source rigour/recency/directness, **0–1**. |
| `bias_risk` | `low` / `medium` / `high`. |
| `supports_claim` | `yes` / `no` / `mixed`. |
| `notes` | Context. **Proposal rows are explicitly labelled HYPOTHESIS ONLY.** |

Note how proposal-sourced rows carry low `quality_score` and `high` `bias_risk` — under CIS they can
*raise* a hypothesis but cannot *validate* it. Consumed by `src/evidence.py` and the dashboards.
