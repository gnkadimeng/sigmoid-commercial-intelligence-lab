---
title: "Commercial Intelligence Specification (CIS)"
subtitle: "A specification for treating commercial strategy as a computational decision system"
version: "0.1.0"
status: "Draft — hypothesis stage"
---

# Commercial Intelligence Specification (CIS)

**Version 0.1.0 · Draft · Governing specification for the Sigmoid Commercial Intelligence Lab.**

This is a technical specification, not marketing material. It defines how commercial strategy is
represented, reasoned about, evidenced, validated, and revised inside this project. Where the
specification and any deck, PDF, or narrative disagree, this specification governs the *process*; the
narrative is treated as input (a hypothesis source), not as an authority.

---

## 1. Introduction

Commercial strategy is normally recorded as prose and slides: assertions about markets, customers,
positioning, and pricing, chosen partly to persuade. Such artifacts are difficult to test, difficult
to revise coherently, and give no account of *why* one recommendation was preferred over another.

The Commercial Intelligence Specification (CIS) defines an alternative: commercial strategy expressed
as a **computational decision system**. Under CIS, strategic claims are structured objects with
identity and provenance; recommendations are outputs of transparent, versioned computation over
evidence; and the entire chain from question to monitored outcome is reproducible.

CIS is deliberately modest at v0.1. It specifies *structure and discipline*, not advanced modelling.
Sophisticated models can be added later without changing the governance contract.

## 2. Purpose

The purpose of CIS is to ensure that every commercial recommendation produced in this project is:

- **Traceable** — it can name the question, hypothesis, and evidence it derives from.
- **Reproducible** — its numbers are produced by code and data anyone can re-run.
- **Falsifiable** — it states what would prove it wrong.
- **Revisable** — it updates coherently as evidence changes, without silent rewriting of history.
- **Honest about confidence** — it distinguishes hypothesis, weak evidence, and validated fact.

## 3. Vision

A commercial strategy that behaves like a well-run experiment programme rather than a fixed argument.
Decisions are versioned. Evidence accumulates. Confidence is measured, not asserted. New information
moves recommendations in a documented way. The organisation can always answer: *what do we believe,
how strongly, and why?*

## 4. Guiding principles

1. **Claims before conclusions.** Nothing is concluded until it has been stated as a falsifiable
   claim and tested.
2. **Evidence over eloquence.** A well-argued assertion with no evidence outranks nothing.
3. **Transparency of computation.** Every score is produced by inspectable code with named weights.
4. **Separation of hypothesis and fact.** The proposal PDF is Hypothesis v0.1; it is never silently
   promoted to evidence.
5. **Weights are data, not code.** Tunable parameters live in YAML/config so they can be changed and
   audited independently of logic.
6. **Reproducibility is non-negotiable.** If a result cannot be re-run, it does not exist.
7. **Confidence is explicit.** Every recommendation carries a confidence grade and its basis.
8. **History is append-only.** Decisions and evidence are superseded, not deleted.
9. **Simplicity first.** Prefer the simplest model that answers the question; defer complexity until
   evidence demands it.

## 5. Scope

**In scope (v0.1):** market prioritisation, CRM positioning, customer/segment fit, AI readiness
assessment, evidence tracking, decision provenance, and the testing standard that guards them.

**Out of scope (v0.1):** live CRM data integration, production ML pipelines, automated data
collection, pricing optimisation at scale, and organisation-wide rollout tooling. These are named in
Future Work and must not be faked with unvalidated numbers.

## 6. Core philosophy

CIS treats a commercial strategy as a **decision system**: a directed process that transforms
**questions** into **monitored recommendations** through explicit, inspectable stages. The unit of
work is not "the strategy" but "the decision" — a single question carried through the lifecycle.

Strategy, in this view, is the accumulated set of decisions plus their evidence and confidence. It is
never finished; it is the current best state of a continuing enquiry.

## 7. Core ontology

The ontology defines the objects the system reasons about. It is specified normatively in
[`cis/ontology.yml`](ontology.yml). Summary:

| Object | Meaning |
|---|---|
| **Question** | A commercial decision to be made, phrased so it can be answered. |
| **Hypothesis** | A falsifiable, provisional answer to a Question. |
| **Operational Definition** | How a hypothesis's terms are measured (what counts, in what units). |
| **Evidence** | A dated, sourced observation that supports, refutes, or qualifies a claim. |
| **Framework** | A named, weighted scoring scheme that turns inputs into a score. |
| **Model** | A computation (framework, statistical model, or rule set) producing an output. |
| **Recommendation** | A proposed action derived from models + evidence, with confidence. |
| **Decision** | A recorded choice to act (or not), with its provenance and owner. |
| **Metric** | A quantity monitored after a decision to test whether it held. |

Relationships (see ontology.yml for cardinality): a Question has many Hypotheses; a Hypothesis has an
Operational Definition and is supported/refuted by Evidence; Frameworks and Models consume Evidence
and produce scores; a Recommendation cites Models and Evidence; a Decision adopts a Recommendation
and is monitored by Metrics.

## 8. Object model

The object model in [`cis/object-model.yml`](object-model.yml) gives each object its fields, types,
identity rule, and required provenance. Normative requirements:

- Every object has a stable `id` and a `version`.
- Every object records `created` and `status` (`draft` → `active` → `superseded`/`retired`).
- Objects that assert something about the world (`Evidence`, `Recommendation`, `Decision`) MUST carry
  provenance: who/what produced them, from which sources, when.
- Scores are stored with the `framework_id` and `framework_version` that produced them, so a score is
  never orphaned from its method.

## 9. Decision lifecycle

The canonical lifecycle, specified in [`cis/decision-lifecycle.yml`](decision-lifecycle.yml):

```text
Question
  → Hypothesis
    → Operational Definition
      → Evidence Collection
        → Analysis
          → Model
            → Validation
              → Recommendation
                → Implementation
                  → Monitoring
                    → Learning ⟲ (feeds back to Question/Hypothesis)
```

Rules:

- A stage MUST NOT be skipped in the recorded provenance. A Recommendation whose provenance lacks
  Evidence and Validation is **invalid** under CIS.
- Each artifact in the repository SHOULD declare the lifecycle stage it advances.
- **Learning** is not a terminus: it revises questions and hypotheses, re-entering the loop. This is
  what makes the strategy "living".

## 10. Evidence model

Evidence is the currency of the system. Specified operationally in `src/evidence.py` and the
`evidence_register.csv` schema.

- Each Evidence item links to a `claim_id` and states `supports_claim ∈ {yes, no, mixed}`.
- Each item has a `quality_score ∈ [0, 1]` (source rigour, recency, directness) and a
  `bias_risk ∈ {low, medium, high}`.
- **Evidence weight** = `quality_score × bias_adjustment`, where bias adjustment penalises higher
  bias risk. Refuting evidence carries the same weight machinery as supporting evidence.
- **Evidence strength** for a claim is a classification (`none / weak / moderate / strong`) derived
  from the aggregate weight of non-conflicting evidence.
- A proposal assertion enters as Evidence only with `source_type = proposal` and is capped in
  quality; it can *raise a hypothesis*, not *validate* one.

## 11. Data model

- **Tabular data** is the primary representation (CSV at v0.1; a database later). Each dataset has a
  documented schema and a README describing provenance and limitations.
- **Sample data is synthetic** and labelled as such. It exists to exercise the machinery, never to
  stand in as market fact.
- Zones: `data/raw` (immutable inputs), `data/processed` (derived, reproducible from raw + code),
  `data/external` (third-party), `data/sample` (synthetic, versioned).
- Identity columns (`segment_id`, `customer_id`, `evidence_id`, `claim_id`) MUST be unique within
  their table.

## 12. Validation model

Two layers, both specified in `src/validation.py` and enforced by `tests/`:

1. **Structural validation** — required columns present, identity columns unique, score columns
   within range `[0, 100]`, no negative scores where the scale forbids them. Optionally enforced with
   `pandera` schemas / `pydantic` models where available.
2. **Decision validation** — a Recommendation is valid only if its provenance includes Evidence and a
   Validation step, and its confidence grade is consistent with the aggregate evidence strength.

Validation failures are errors, not warnings: they block promotion of a score or recommendation.

## 13. Decision provenance

Every Decision records:

- the `question_id` it answers and the `recommendation_id` it adopts;
- the `models` and `evidence` cited, each by `id` and `version`;
- the `owner` (accountable person/role) and the `date`;
- the `confidence` grade and the `basis` for it;
- the `status` (`proposed / adopted / superseded / reversed`).

Provenance is what allows the project to answer "why did we decide this, on what basis, and has it
changed?" without archaeology.

## 14. Governance

- CIS governs process; it does not dictate conclusions.
- Changes to CIS itself are made through **Architecture Decision Records** (`docs/decision-records/`)
  and version bumps to this document.
- Framework weight changes are versioned in the framework YAML and require a note of rationale.
- No artifact may present an unvalidated number as validated. Reviewers enforce this.
- The append-only rule applies to Decisions, Evidence, and ADRs.

## 15. Computational architecture

```text
data/ (CSV, synthetic sample)      frameworks/ (YAML weights)      cis/ (ontology, lifecycle)
        │                                   │                              │
        └───────────────┬───────────────────┴──────────────┬──────────────┘
                        ▼                                   ▼
                    src/  (scoring · validation · evidence · ontology · utils)
                        │
          ┌─────────────┼──────────────┐
          ▼             ▼              ▼
      tests/       dashboards/*.qmd   working-paper/*.qmd
   (pytest guards)  (Plotly, live)     (structured enquiry)
                        │
                        ▼
                  Quarto site (_site/)
```

- **`src/`** is the single source of computational truth. Dashboards and notebooks import from it;
  they do not re-implement scoring.
- **`frameworks/`** holds tunable parameters as data.
- **`tests/`** guards `src/` and data integrity; nothing downstream is trusted if tests fail.

## 16. Testing standard

- Every scoring function MUST be tested for: output range `[0, 100]`, missing-value safety, and
  monotonicity/sanity on at least one clear case.
- Every validation function MUST be tested on both a passing and a failing input.
- Evidence classification and aggregation MUST be tested against known inputs.
- Sample datasets MUST have an integrity test (required columns present, ids unique, scores in
  range). The suite runs with `pytest` and must be green before results are trusted.

## 17. Decision confidence

Every Recommendation carries a confidence grade:

| Grade | Meaning | Typical basis |
|---|---|---|
| **D — Hypothesis** | Asserted, not yet evidenced. | Proposal claim only. |
| **C — Indicative** | Weak evidence, illustrative computation. | Sample/synthetic data, single source. |
| **B — Substantiated** | Moderate, corroborated evidence. | Multiple independent sources, validated method. |
| **A — Validated** | Strong evidence, method validated, monitored. | Convergent evidence + live metrics. |

At v0.1 essentially everything is grade **C or D**. A recommendation's grade MUST NOT exceed what its
aggregate evidence strength (see §10) supports.

## 18. Continuous learning

The Monitoring and Learning stages close the loop. Post-decision `Metric` observations are compared
to the expectations the Recommendation stated. Divergence triggers revision: hypotheses are updated,
evidence re-weighted, and, if needed, the Question re-opened. Learning is recorded, so the project has
memory of what changed and why.

## 19. Extension model

CIS is extended without breaking the governance contract by:

- **New frameworks** — add a YAML file + scoring function + test; register its question.
- **New objects** — extend `ontology.yml` and `object-model.yml` with a version bump; add an ADR.
- **New models** — a statistical/ML model is a `Model` object; it must still pass through Validation
  and carry provenance. Advanced ML does not bypass the lifecycle.
- **New data sources** — documented schema + README + integrity test.

Extensions MUST preserve: traceability, reproducibility, the hypothesis/fact separation, and the
testing standard.

## 20. Success criteria

CIS is succeeding when:

1. Every published recommendation can name its lifecycle provenance and confidence grade.
2. No unvalidated claim is presented as fact.
3. Re-running the repository reproduces every score and figure.
4. The test suite is green and covers all scoring/validation/evidence logic.
5. Evidence accumulates over time and visibly moves recommendations.
6. A newcomer can trace any conclusion back to its question and evidence unaided.

## 21. Future work

- Live CRM / RevOps data integration replacing synthetic samples.
- `pandera`/`pydantic` schemas enforced in CI on real data.
- Segmentation models (`scikit-learn`) as first-class `Model` objects.
- Pricing and willingness-to-pay models with proper elasticity evidence.
- A persistent decision store (database) with provenance queries.
- Automated confidence-grade computation from the evidence register.
- Knowledge-graph representation of the ontology (`networkx` → graph DB).

---

*Document status:* **v0.1.0, Draft.** This specification will itself evolve through ADRs and version
bumps. Its authority is over *process*; conclusions remain earned through evidence.
