# Sigmoid Commercial Intelligence Lab

A reproducible research and decision-intelligence project that converts the Sigmoid Analytica
investor/operator proposal into a **living Commercial Intelligence Lab** — where commercial strategy
becomes evidence-based, versioned, testable, and interactive.

The project is governed by the **Commercial Intelligence Specification (CIS)**, which treats
commercial strategy as a computational decision system. The source proposal PDF is treated as
**Hypothesis v0.1**, not as validated fact.

---

## 1. Project purpose

Turn strategic claims (which market to target, how to position the CRM, what customers will pay) into
falsifiable questions that are answered with evidence through a fixed decision lifecycle:

```text
Question → Hypothesis → Operational Definition → Evidence Collection → Analysis
        → Model → Validation → Recommendation → Implementation → Monitoring → Learning
```

The lab provides transparent scoring frameworks, an evidence register, interactive dashboards, a
working paper, and an automated test suite that guards every calculation.

## 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Render the Quarto site

```bash
quarto render                       # build the full site into _site/
quarto preview                      # live preview with hot reload
```

You need [Quarto](https://quarto.org) installed and a Python kernel (`ipykernel`) on the active
virtual environment.

## 4. Run the tests

```bash
pytest
```

All scoring, validation, and evidence logic is covered. Tests must pass before any framework or
score is considered trustworthy.

## 5. Project structure

```text
sigmoid-commercial-intelligence-lab/
├── cis/                 # Commercial Intelligence Specification + ontology/object/lifecycle YAML
├── working-paper/       # Evidence-building working paper (one open question per chapter)
├── frameworks/          # Versioned, weighted scoring frameworks (YAML)
├── data/                # raw / processed / external / sample (synthetic) datasets
├── notebooks/           # Exploratory Jupyter notebooks
├── src/                 # Python modules: scoring, validation, evidence, ontology, utils
├── tests/               # pytest suite
├── dashboards/          # Interactive Quarto pages (Plotly)
├── references/          # Bibliography + source log
├── assets/              # CSS, figures
└── docs/decision-records/  # Architecture Decision Records (ADRs)
```

## 6. Current status

**v0.1 — hypothesis stage.** The architecture, frameworks, sample data, scoring logic, tests, and
dashboards exist and run. **No recommendation is validated.** All scores and rankings are
illustrative until the underlying claims pass through the evidence and validation stages of the CIS
lifecycle. Sample datasets are synthetic.

## 7. How collaborators should contribute

1. Fork/branch from `main`; one logical change per branch.
2. Keep the CIS lifecycle honest: state which lifecycle stage your change advances.
3. Run `pytest` before opening a pull request; add tests for new scoring or validation logic.
4. Do not introduce "validated" conclusions without an evidence trail in the register.
5. Prefer editing framework **weights in YAML** over hard-coding numbers in analysis pages.

## 8. How to add new evidence

1. Add a row to `data/sample/evidence_register.csv` (or your working register) with a unique
   `evidence_id`, the `claim_id` it supports/refutes, `source_type`, `quality_score` (0–1),
   `bias_risk`, and `supports_claim` (`yes`/`no`/`mixed`).
2. Mark unvalidated items honestly — a proposal assertion is a **hypothesis**, not evidence.
3. Re-run the relevant dashboard/notebook; evidence weight and strength are recomputed by
   `src/evidence.py`.
4. If the claim is new, register the question/hypothesis in the working paper chapter it belongs to.

## 9. How to add a new framework

1. Create `frameworks/<name>.yml` following the shape of the existing frameworks
   (`id`, `version`, `question`, `criteria` with `weight` + `direction`, `scale`, `status`).
2. Ensure the weights sum to 1.0 (or document the normalisation rule).
3. If it introduces a new score, add a scoring function to `src/scoring.py` and a test to
   `tests/test_scoring.py` asserting the 0–100 range and missing-value safety.
4. Reference the framework from a dashboard and/or working-paper chapter.

## 10. How to add a new decision record

1. Copy an existing ADR in `docs/decision-records/` to `ADR-XXXX-<slug>.md` (next number).
2. Use the standard headings: Status, Context, Decision, Consequences, Alternatives considered.
3. Link it from `docs/decision-records/index.qmd`.
4. ADRs are append-only: supersede rather than delete.

---

## How to Add Real Evidence

The **Evidence Operating Layer** turns real customer discovery into structured evidence that moves
claims and, in turn, decisions. The flow is: **interview → evidence record → claim → decision**. The
registers are the single source of truth; the decision and claims pages recompute from them.

> **Rules:** do not invent real evidence, do not mark anything as validated, and keep the project at
> v0.1 hypothesis stage. A claim only reaches grade **B** when multiple independent, low-bias items
> converge — one interview is never enough.

1. **Complete a discovery interview.** Use `templates/discovery_interview_template.md` to run it and
   score the signals honestly (including `evidence_quality_score` and `bias_risk`).
2. **Add the interview** as one row in `data/raw/discovery_interviews.csv` (schema columns:
   `interview_id … supports_or_refutes`).
3. **Map the interview to claims** by adding one row per claim to
   `data/processed/discovery_evidence.csv`, using `templates/evidence_capture_template.md`. Each row
   links an `evidence_id` to a `claim_id` (from `data/sample/claim_register.csv`) and a `decision_id`.
4. **Run the tests:**

   ```bash
   pytest
   ```

   The validators check required columns, that confidence grades are only A/B/C/D, that
   `supports_or_refutes` is only supports/refutes/mixed/neutral, and that score fields are in range.
5. **Render the site:**

   ```bash
   quarto render
   ```

6. **Review whether claim confidence changed.** Open **Evidence → Claims & Confidence** and the
   relevant **Decision** page; the real-evidence counts recompute from your new records.
7. **Update decision status if needed.** If a claim clears its `evidence_needed_for_B`, update that
   claim's `current_confidence_grade` in `data/sample/claim_register.csv` and the decision's
   `current_status` / `current_confidence_grade` in `data/sample/decision_register.csv`. Record *why*
   (an ADR or a note) — grade changes are decisions, not edits.

**Registers at a glance**

| File | Role |
|---|---|
| `data/sample/decision_register.csv` | The three decisions, their status, confidence, and required grade |
| `data/sample/claim_register.csv` | The hypotheses behind each decision, and what evidence each needs |
| `data/raw/discovery_interviews.csv` | Raw fieldwork — one row per interview |
| `data/processed/discovery_evidence.csv` | Evidence records mapping interviews → claims → decisions |

---

## Quick reference

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
quarto render
quarto preview
```

## License & data note

Sample data is **synthetic** and for demonstration only. Nothing in this repository should be cited
as a validated market fact at v0.1.
