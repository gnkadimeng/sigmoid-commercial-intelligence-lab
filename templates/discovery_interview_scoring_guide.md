# Discovery Interview Scoring Guide — First Evidence Sprint

Score every interview **the same day**, while it is fresh. All scores below are captured on a **0–100**
scale in `data/raw/discovery_interviews.csv`. This guide gives anchored bands so two interviewers score
the same conversation similarly.

> **Score conservatively.** When unsure, score lower. A single interview is weak evidence by nature —
> the model is designed so that only *convergent, low-bias* evidence moves a claim. Do not inflate
> scores to make a segment look attractive.

**Anchor points** used throughout: **0** = absent, **25** = weak, **50** = moderate, **75** = strong,
**100** = unambiguous/severe. Interpolate freely.

---

## Signal scores (0–100)

### `pain_score` — how acute and specific is the pain
- **0–20** No real pain; "we manage fine."
- **21–40** Mild annoyance; generic grumbling, no cost attached.
- **41–60** Real, recurring pain named specifically, but tolerated.
- **61–80** Acute pain with a felt cost (time, rework, lost work) and frequency.
- **81–100** Severe, frequent, costed pain the respondent raised unprompted.
- *Claims:* H-SEG-AUDIT-01, H-SEG-PROF-01 (D1).

### `budget_signal` — is there money and a buyer
- **0–20** No budget, no owner, "we wouldn't pay for this."
- **21–40** Vague interest, no budget line identified.
- **41–60** A plausible owner named; budget "might exist."
- **61–80** Clear budget owner + budget this year + prior spend on adjacent tools.
- **81–100** Active budget, named buyer, explicit intent to allocate.
- *Claim:* H-SEG-AUDIT-02 (D1).

### `urgency_signal` — is there a reason to act now
- **0–20** "Someday" problem; no timeline.
- **21–40** Would like to fix eventually.
- **41–60** On the roadmap, no compelling event.
- **61–80** This-quarter priority with a driver (growth, audit season, a failure).
- **81–100** Urgent, compelling event with a deadline.
- *Claim:* H-SEG-AUDIT-01 (D1).

### `crm_maturity` — sophistication and adoption of current CRM
- **0–20** Spreadsheets / email only; no CRM.
- **21–40** A CRM exists but is barely used.
- **41–60** CRM used by some of the team, inconsistently.
- **61–80** CRM well-adopted across the commercial team.
- **81–100** Mature, disciplined CRM practice with clean data.
- *Claims:* H-POS-CRM-01, H-AI-READY-02 (D2).

### `workflow_maturity` — how defined and standardised the commercial workflow is
- **0–20** Ad hoc; everything person-dependent.
- **21–40** Loose conventions, not written down.
- **41–60** Defined process, unevenly followed.
- **61–80** Standardised, documented, mostly followed.
- **81–100** Fully standardised and instrumented.
- *Claim:* H-AI-READY-02 (D2).

### `ai_readiness_maturity` — data structure + analytics practice
- **0–20** Data scattered; no analytics.
- **21–40** Some reports, mostly manual, data siloed.
- **41–60** Structured data in places; basic dashboards.
- **61–80** Clean, centralised data; regular analytics.
- **81–100** Strong data foundation, ready to operationalise AI.
- *Claims:* H-AI-READY-01, H-AI-READY-02 (D2).

### `willingness_to_pay_signal` — directional price reaction
- **0–20** Would not pay; expects free.
- **21–40** Would pay only a token amount.
- **41–60** Open to paying; no figure given.
- **61–80** Named a plausible monthly figure at/near expectations.
- **81–100** Named a figure at or above target, with conviction.
- *Claim:* H-SEG-AUDIT-02 (D1). *Keep directional — do not anchor the respondent.*

### `sales_cycle_signal` — ease/speed of buying (higher = shorter and simpler)
- **0–20** Very long cycle, many sign-offs, procurement-heavy.
- **21–40** Long cycle, committee decision.
- **41–60** Moderate; a couple of stakeholders.
- **61–80** Short; one or two decision-makers.
- **81–100** Fast; a single owner can decide.
- *Claim:* H-GTM-GATE-01 (D1/D3). *Note the inversion: high score = easy to buy.*

---

## Evidence-quality scores (0–100)

### `evidence_quality_score` — how much weight this single source deserves
Judges rigour, directness, and recency of *this* interview.
- **0–20** Hearsay, off-topic, or a very junior/uninformed respondent.
- **21–40** Relevant but indirect; respondent generalising.
- **41–60** Direct, first-hand account from a relevant role (typical ceiling for one discovery call).
- **61–80** First-hand, decision-maker, specific and corroborated within the call.
- **81–100** Rare for an interview — reserve for documented, verifiable evidence.
- *A one-off discovery call should seldom exceed **50**.*

### `bias_risk` — how much this evidence may be distorted (higher = more biased = worse)
Consider: did we lead the witness? Is the respondent incentivised to please us? Selection bias in who
we reached? Recall bias?
- **0–20** Low risk: neutral questioning, disinterested respondent, representative selection.
- **21–40** Some risk: minor leading, friendly respondent.
- **41–66** Medium risk: warm intro, respondent wants to help us, some leading.
- **67–85** High risk: clearly leading, respondent invested in our success.
- **86–100** Severe: respondent is a friend/investor, or answers were coached.

---

## Direction: `supports_or_refutes`

For each claim the interview touches, decide the direction (recorded in the interview row for the
primary claim, and per-claim in the evidence records):

- **supports** — the evidence makes the claim more likely true.
- **refutes** — the evidence makes the claim less likely true.
- **mixed** — genuinely cuts both ways.
- **neutral** — touched on but uninformative.

---

## Converting raw scores → processed evidence records

`data/processed/discovery_evidence.csv` uses the conventions the evidence model expects. Convert as
follows when you create evidence records (see `templates/evidence_capture_template.md`):

| Raw interview field (0–100) | Processed evidence field | Conversion |
|---|---|---|
| `evidence_quality_score` | `quality_score` | divide by 100 → **0.0–1.0** |
| `bias_risk` | `bias_risk` | band → **`low`** (0–33) · **`medium`** (34–66) · **`high`** (67–100) |
| `supports_or_refutes` | `supports_or_refutes` | copy unchanged (supports / refutes / mixed / neutral) |

The 0–100 signal scores (`pain_score`, `budget_signal`, …) stay in the **interview** row; they inform
your narrative `evidence_summary` and `confidence_impact` but are not re-stored in the evidence record.

> **Reminder.** These scores describe *one source*. Confidence grades in the registers change only by
> deliberate review when the `evidence_needed_for_B` bar is met by multiple independent, low-bias
> items — never automatically, and never from a single interview.
