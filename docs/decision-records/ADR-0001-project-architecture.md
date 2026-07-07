# ADR-0001: Project architecture

::: {.chapter-chips}
<span class="chip chip-grade-a">Status · Accepted</span>
<span class="chip chip-neutral no-dot">2026-07-03</span>
<span class="chip chip-neutral no-dot">Supersedes · none</span>
:::

- **Status:** Accepted
- **Date:** 2026-07-03
- **Deciders:** Sigmoid Commercial Intelligence Lab
- **Supersedes:** —

## Context

We are converting a commercial-strategy proposal into a reproducible, collaborative, testable
research project — not a slide deck or a static document site. The architecture must let strategy be
questioned, computed, tested, and revised as evidence accumulates, and must keep unvalidated numbers
from being mistaken for findings.

## Decision

Adopt the following stack and structure:

- **Quarto (website project)** — one artifact renders the working paper, dashboards, frameworks, CIS,
  and decision records together; prose and executable analysis live side by side and stay in sync.
- **Python + Jupyter execution for `.qmd`** — analysis is code, re-run on every render; results are
  reproducible rather than pasted.
- **Pandas + Plotly** — tabular data handling and interactive charts with a light dependency set.
- **A `src/` package as the single source of computational truth** — scoring, validation, evidence,
  and ontology logic implemented once and imported by dashboards, notebooks, and tests. No
  re-implementation of scoring in analysis pages.
- **YAML specifications** (`cis/`, `frameworks/`) — ontology, object model, lifecycle, and framework
  **weights are data**, editable and auditable independently of code.
- **Synthetic sample data** (`data/sample/`) — exercises the machinery and renders the site without
  claiming any real market fact; raw/processed/external zones are reserved for real data later.
- **Modular scoring functions with dictionary weights** — transparent, tunable, and individually
  testable; every score is a pure function returning `[0, 100]`.
- **Pytest** — scoring ranges, missing-value safety, validation, evidence aggregation, and data
  integrity are all under automated test; a red suite is a hard stop.
- **Git-friendly layout** — small text files, clear boundaries, append-only decision records.

## Consequences

**Positive**

- Any number can be traced to the code, data, and framework that produced it, and re-run.
- Contributors change behaviour by editing weights/data, not by rewriting analysis prose.
- Tests catch regressions in the load-bearing logic before results are trusted.
- The same repository serves reviewers, analysts, and architects.

**Negative / costs**

- Contributors need Python + Quarto installed; a pure-Markdown contributor cannot touch the analysis.
- Keeping the scoring weight dicts in `src/` in sync with the framework YAML is a manual discipline
  at v0.1 (mitigated by `utils.weights_from_framework` and tests).

## Alternatives considered

- **A static docs site (MkDocs/plain Markdown).** Rejected: no executable analysis, no reproducibility,
  and it would invite pasted, un-checkable numbers.
- **A notebook-only project.** Rejected: notebooks are hard to review and diff, and encourage logic
  duplicated across cells rather than a tested shared core.
- **A BI dashboard tool.** Rejected at v0.1: heavier, less version-controllable, and it separates the
  reasoning (prose) from the computation.
