# CIS Compliance Checklist — Template

**CIS basis:** §11 Provenance · §14 Testing · §18 Success Criteria
**Job:** Assure — confirm an artifact (or a whole project) is CIS-compliant before it ships or informs
a decision.
**How to use:** copy per artifact or per milestone; tick each item or record the gap.

---

## Subject

| Field | Value |
|---|---|
| Artifact / project |  |
| Reviewer (§12) |  |
| Date |  |

## Principles (§2)

- [ ] Every component supports a business decision (Principle 1)
- [ ] Every recommendation is backed by identifiable evidence (Principle 2)
- [ ] Every strategic concept has an operational definition (Principle 3)
- [ ] Every framework can be tested (Principle 4)
- [ ] Every recommendation explains why / on what evidence / which framework / what confidence (Principle 5)
- [ ] History is versioned; nothing overwritten (Principle 6)
- [ ] The artifact can improve as new evidence arrives (Principle 7)

## Provenance (§11) — every recommendation must answer

- [ ] Why was this recommended?
- [ ] Which evidence supported it? (ids listed)
- [ ] Which model generated it? (id listed)
- [ ] Which assumptions remain?
- [ ] When was it last reviewed?
- [ ] Chain is complete: Recommendation → Framework → Model → Dataset → Evidence → Source

## Object hygiene (§6, §9, §12)

- [ ] Every object has a stable `id` and `version`
- [ ] No hidden variables — all framework/model inputs declared (§9)
- [ ] Frameworks define logic only; calculation lives in Models (§6.3 / §6.4)
- [ ] Governance set on every object: owner · reviewer · approver (§12)
- [ ] Confidence is explicit and never binary (§15)

## Testing (§14)

- [ ] Every framework/model has automated tests
- [ ] Tests currently pass (attach run / date)

## Success criteria (§18)

- [ ] Recommendations are reproducible
- [ ] Complete evidence traceability
- [ ] Automated validation supported
- [ ] Continuous improvement supported
- [ ] Every recommendation explained
- [ ] Knowledge separated from computation
- [ ] Version history maintained
- [ ] Collaborative development supported
- [ ] Heterogeneous data sources integrated
- [ ] AI-assisted reasoning without losing explainability

## Result

| Field | Value |
|---|---|
| Items passed | __ / total |
| Blocking gaps |  |
| Compliant? | Yes / No / Conditional |
| Sign-off (name, date) |  |
