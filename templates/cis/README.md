# CIS Templates

Reusable templates for producing artifacts that comply with the
[Commercial Intelligence Specification (CIS)](../../cis/commercial-intelligence-specification.md).
Each template maps 1:1 to a section of the standard, so a filled-in template *is* a CIS-compliant
object.

> **Principle 1 (CIS §2):** documentation that does not support a business decision should not exist.
> Every template here earns its place by producing, assuring, or communicating a decision.

## The five jobs a template can do

| Job | Purpose | Templates here | CIS basis |
|---|---|---|---|
| **Author** | Create *one* compliant object | `objects/*.template.yml` | §5 Ontology, §6 Object Model, §8 Evidence |
| **Assure** | Prove quality before deciding | `assurance/*.template.md` | §10 Validation, §14 Testing, §18 Success |
| **Communicate** | Present the decision to humans | `communicate/*.template.md` | §13 Presentation, §15 Confidence |
| **Track** | Hold *many* objects over time | *(already in the lab)* `data/sample/*_register.csv` | §11 Provenance, §12 Governance |
| **Collect** | Gather raw field inputs | *(already in the lab)* `templates/discovery_interview_*` | §8 Evidence, §9 Data |

*Track* and *Collect* are covered by the lab's existing registers and discovery instruments — this
folder fills the **Author**, **Assure**, and **Communicate** gaps.

## Canonical form

The CIS defines every object as **YAML metadata** (§6/§8). So the object templates are **YAML** — the
authoritative, machine-readable, version-controllable, testable form that the computational system and
AI agents (§13 Presentation layer) consume. Branded Word/PDF renderings for clients and partners are a
downstream on-ramp over the *same* fields.

## Contents

```text
templates/cis/
├── objects/                              # Author — one object per file
│   ├── question.template.yml             # §6.1
│   ├── hypothesis.template.yml           # §6.2
│   ├── framework.template.yml            # §6.3
│   ├── model.template.yml                # §6.4
│   ├── evidence.template.yml             # §8
│   └── recommendation.template.yml       # §6.5, §11, §15
├── assurance/                            # Assure
│   ├── validation-report.template.md     # §10 (six levels)
│   └── cis-compliance-checklist.template.md  # §14 + §18 + §11
└── communicate/                          # Communicate
    └── recommendation-brief.template.md  # §11 + §15
```

## How to use

1. **Copy**, don't edit in place: `cp objects/question.template.yml questions/Q-001.yml`.
2. **Fill every field.** A blank required field is a compliance failure — hidden variables are
   prohibited (§9).
3. **Register** the object's `id` in the matching register (`data/sample/*_register.csv`).
4. **Assure** before deciding: complete a validation report and run the compliance checklist.
5. **Communicate** with a recommendation brief that carries confidence and full provenance.

## Governance (§12)

Every object carries a `governance` block with **owner · reviewer · approver · version ·
dependencies**. Decide who fills each role — and, where two companies co-deliver, which entity holds
each. History is append-only: supersede, never overwrite (§2, Principle 6).

## Confidence (§15)

Recommendations are never binary. Use either the lab's letter grades — **D** (hypothesis) · **C**
(indicative) · **B** (substantiated) · **A** (validated) — or a 0.00–1.00 score, consistently across a
project. Nothing reaches A/high without convergent evidence and operational validation (§10).
