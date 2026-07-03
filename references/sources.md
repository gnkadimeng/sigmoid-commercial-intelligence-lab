# Sources log

A human-readable log of sources feeding the project, and their status under the CIS evidence model.
The machine-readable version of *evidence* is [`data/sample/evidence_register.csv`](../data/sample/evidence_register.csv);
this file adds narrative context and tracks sources we intend to consult.

> **Reminder:** a source being *listed* here says nothing about its reliability. Quality and bias are
> recorded per evidence item in the register.

## Primary source (Hypothesis v0.1)

| Source | Type | Status | Notes |
|---|---|---|---|
| Sigmoid Analytica Proposal PDF | proposal | Hypothesis v0.1 (grade D) | The document this project interrogates. Not evidence. |

## Consulted / registered evidence

See the [evidence register](../data/sample/evidence_register.csv) for the current items (`EV-001` …).
At v0.1 these are synthetic/illustrative except where a real source is named.

## Sources to obtain (evidence backlog)

- [ ] Competitor pricing and positioning benchmarks (per candidate segment).
- [ ] Independent market-size / SME statistics (national sources) for `data/external/`.
- [ ] Discovery-call notes for the top 2 segments (Ch. 5).
- [ ] Message-testing results for the three positioning framings (Ch. 4).
- [ ] Post-pilot AI-value outcomes to test H-CRM-AI (Ch. 6).

## How to add a source

1. If it produces evidence, add a row to the evidence register with quality + bias metadata.
2. If it is a citable work, add a BibTeX entry to `bibliography.bib`.
3. Note licensing/attribution for any third-party data placed in `data/external/`.
