# ADR-0002: CIS as the governance model; the PDF as a hypothesis source

- **Status:** Accepted
- **Date:** 2026-07-03
- **Deciders:** Sigmoid Commercial Intelligence Lab
- **Supersedes:** —
- **Related:** [ADR-0001](ADR-0001-project-architecture.md)

## Context

The project's inputs include a persuasive investor/operator proposal. Persuasive documents are
written to argue a position *before* the evidence is in, and they mix genuine insight with untested
assumptions about market, positioning, and pricing. We need an explicit rule for how such a document
enters the project, and a governing model that keeps recommendations honest as evidence accumulates.

## Decision

1. **Adopt the Commercial Intelligence Specification (CIS) as the governance model** for the project.
   CIS treats commercial strategy as a computational decision system with a fixed lifecycle
   (Question → … → Monitoring → Learning), a typed ontology and object model, an evidence model, a
   validation model, confidence grades (D–A), and a testing standard.

2. **Treat the proposal PDF as Hypothesis v0.1 — a hypothesis *source*, not validated evidence.**
   Its claims are extracted into falsifiable hypotheses and registered as evidence of
   `source_type = proposal`, capped at low quality and high bias risk. Under the evidence model such
   items can *raise* a hypothesis but cannot lift a claim above confidence grade C on their own.

3. **CIS governs process, not conclusions.** It dictates how claims are evidenced, validated, and
   graded — never what the answer must be. Where narrative and specification disagree about *process*,
   the specification wins; the narrative remains an input.

## Consequences

**Positive**

- No claim — however well-argued in the proposal — is presented as fact without an evidence trail.
- Confidence is explicit and bounded by evidence strength, so readers can calibrate trust.
- The strategy becomes revisable: as evidence arrives, grades and recommendations change in a
  documented way rather than by silent rewriting.
- Reviewers have a concrete standard to enforce ("what stage, what evidence, what grade?").

**Negative / costs**

- More upfront discipline: every recommendation must name its provenance and grade.
- It can feel slow to stakeholders expecting immediate answers from a compelling deck; this is the
  intended trade of speed for defensibility.

## Alternatives considered

- **Treat the proposal as the project's conclusions and build support around it.** Rejected: this
  bakes in untested assumptions and defeats the purpose of an evidence-based lab.
- **Ad-hoc review with no formal model.** Rejected: without a fixed lifecycle and confidence scale,
  "how sure are we?" gets answered inconsistently, and unvalidated numbers leak into decisions.

## Notes

Changes to CIS itself are made through new ADRs and version bumps to
`cis/commercial-intelligence-specification.md`. This record is append-only; supersede rather than
edit.
