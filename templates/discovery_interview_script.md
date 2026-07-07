# Discovery Interview Script — First Evidence Sprint

**Segments:** Audit firms · Professional services firms
**Duration:** ~40 minutes
**Instrument version:** v0.1 (first sprint)

This is the field script for the first real evidence sprint. It maps every question to the
**decision register** (`data/sample/decision_register.csv`), the **claim register**
(`data/sample/claim_register.csv`), and the **fields** of `data/raw/discovery_interviews.csv`. After
the call, score the interview with `templates/discovery_interview_scoring_guide.md` and turn it into
evidence records with `templates/evidence_capture_template.md`.

> **Rules for the interviewer.** Do not lead the witness. Ask open questions first, probe second.
> Record what the respondent actually said (verbatim where possible) in `notes`. One interview is a
> single data point — it never validates a claim on its own. **Do not invent answers; leave a field
> blank if it was not covered.**

**Legend:** each question shows → *Decision* · *Claim(s)* · *`csv_field`* · *scoring note*.

---

## 0. Interviewer setup (before the call)

- Assign `interview_id` (e.g. `INT-0001`), record `date` (`YYYY-MM-DD`).
- Confirm the segment: `company_segment` = `Audit` or `Professional Services`.
- Primary decision under test this sprint: **D1 (Market Entry)** and **D2 (Positioning)**.

Open neutrally: *"We're researching how firms like yours run commercial and client operations. There
are no right answers — we're trying to learn, not sell. May I take notes?"*

---

## 1. Respondent context

*Purpose: establish who is speaking and how much weight their view carries (feeds `bias_risk` and
`evidence_quality_score`).*

**Q1.1 — "Tell me about your firm and your role in it."**
- *Why:* sizing and authority; a partner's budget view differs from an analyst's.
- → context · — · `company_size`, `respondent_role` · capture band + role verbatim.

**Q1.2 — "How many people touch client acquisition or delivery operations?"**
- *Why:* scale of the workflow problem.
- → D1 · H-SEG-PROF-01 · `notes` · qualitative.

---

## 2. Current commercial process

*Purpose: understand how they actually win and deliver work today — the substrate a CRM would
organise.*

**Q2.1 — "Walk me through how a new client goes from first contact to signed engagement."**
- *Why:* reveals pipeline structure (or its absence) and hand-off pain.
- → D1 · H-SEG-PROF-01 · `notes`, contributes to `workflow_maturity`.

**Q2.2 — "Where in that process do things most often slip or get lost?"**
- *Why:* locates the acute pain without naming it for them.
- → D1 · H-SEG-AUDIT-01, H-SEG-PROF-01 · `notes`, contributes to `pain_score`.

---

## 3. Current tooling

*Purpose: what they use now, and how mature it is.*

**Q3.1 — "What tools do you use to track clients, pipeline, and work in progress?"**
- *Why:* baseline; distinguishes spreadsheet-shops from CRM-shops.
- → D1/D2 · H-POS-CRM-01, H-AI-READY-01 · `current_tooling` (free text) → informs `crm_maturity`.

**Q3.2 — "What do those tools do well, and where do they fall short?"**
- *Why:* separates a tooling-gap from a discipline-gap.
- → D1 · H-SEG-PROF-01 · `notes`.

---

## 4. Pain points

*Purpose: the core of D1 — is there acute, specific, felt pain?*

**Q4.1 — "What's the single most frustrating part of running your commercial workflow?"**
- *Why:* the headline pain, in their words.
- → D1 · **H-SEG-AUDIT-01** (audit), **H-SEG-PROF-01** (prof. services) · `notes` → `pain_score`.

**Q4.2 — "How often does that happen, and who does it affect?"**
- *Why:* frequency and blast radius separate a nuisance from a priority.
- → D1 · H-SEG-AUDIT-01 · contributes to `pain_score`.

---

## 5. Cost of pain

*Purpose: convert pain into money/time — the bridge from pain to budget and urgency.*

**Q5.1 — "If you had to estimate, what does that problem cost you — in hours, missed work, or
rework?"**
- *Why:* quantifies pain; a costed problem is a fundable one.
- → D1 · H-SEG-AUDIT-01, **H-SEG-AUDIT-02** · `notes` → raises `pain_score` and `budget_signal`.

**Q5.2 — "Has anyone tried to fix it before? What happened?"**
- *Why:* prior spend signals real budget and reveals switching costs.
- → D1 · H-SEG-AUDIT-02 · `notes` → `budget_signal`.

---

## 6. CRM / workflow maturity

*Purpose: score how defined and adopted their processes and CRM are (feeds D2 AI-readiness thesis).*

**Q6.1 — "How standardised are your commercial workflows — same every time, or person-dependent?"**
- *Why:* defined workflows are what a CRM (and later AI) can act on.
- → D2 · H-AI-READY-02 · `workflow_maturity` · score 0–100.

**Q6.2 — "If you have a CRM today, how much of the team actually lives in it?"**
- *Why:* adoption, not ownership, is the real maturity signal.
- → D2 · H-POS-CRM-01, H-AI-READY-02 · `crm_maturity` · score 0–100.

---

## 7. Analytics / AI readiness

*Purpose: test the AI-readiness claims — do they have structured data, and would a CRM improve it?*

**Q7.1 — "How do you currently use your data to make commercial decisions?"**
- *Why:* existing analytics practice predicts ability to operationalise AI.
- → D2 · **H-AI-READY-01** · `ai_readiness_maturity` · score 0–100.

**Q7.2 — "Is your client and pipeline data structured and in one place, or scattered?"**
- *Why:* directly tests H-AI-READY-01 (customers may lack structured data).
- → D2 · **H-AI-READY-01** · `notes` → `ai_readiness_maturity`.

**Q7.3 — "If your CRM were well-adopted, do you think it would make you more 'AI-ready'? Why?"**
- *Why:* tests H-AI-READY-02 (CRM implementation may improve AI readiness). Probe reasoning, not a
  yes/no.
- → D2 · **H-AI-READY-02** · `notes`.

---

## 8. Budget signal

*Purpose: is there money and a buyer? (D1 · H-SEG-AUDIT-02.)*

**Q8.1 — "Who would own the budget for a tool like this, and is there budget this year?"**
- *Why:* identifies buyer + budget line; distinguishes interest from intent.
- → D1 · **H-SEG-AUDIT-02** · `budget_signal` · score 0–100.

---

## 9. Urgency signal

*Purpose: is there a compelling reason to act now? (D1.)*

**Q9.1 — "Is this a 'this quarter' problem or a 'someday' problem? What makes it urgent, or not?"**
- *Why:* urgency drives the deal; absence of it predicts stall.
- → D1 · H-SEG-AUDIT-01 · `urgency_signal` · score 0–100.

---

## 10. Sales cycle & decision complexity

*Purpose: how hard/long is it to buy? (D1 sequencing, D3 gate.)*

**Q10.1 — "If you decided to adopt something, how long would it take and who would need to sign off?"**
- *Why:* short cycles and few stakeholders make a better first segment.
- → D1/D3 · H-GTM-GATE-01 · `sales_cycle_signal` · score 0–100 (higher = shorter/simpler).

---

## 11. Positioning test

*Purpose: test how the three framings land. Use the full script in
`templates/positioning_message_test.md`; record the outcome here.*

**Q11.1 — Read the three one-line descriptions (CRM / Revenue Operations / AI Readiness) and ask:
"Which of these sounds most like something your firm needs — and why?"**
- *Why:* tests the D2 positioning claims against a real buyer.
- → D2 · **H-POS-CRM-01, H-POS-REVOPS-01, H-POS-AI-01** · `positioning_preference` (`CRM` / `RevOps`
  / `AI Readiness` / `unclear`).

**Q11.2 — "Is there anything in those that sounds overpromised or not credible?"**
- *Why:* tests H-POS-AI-01 (AI framing may overpromise).
- → D2 · H-POS-AI-01 · `notes`.

**Q11.3 (optional WTP probe) — "If one of those solved your headline problem, what would that be worth
per month to your firm?"**
- *Why:* light willingness-to-pay read; keep it directional, do not anchor.
- → D1/D3 · H-SEG-AUDIT-02 · `willingness_to_pay_signal` · score 0–100.

---

## 12. Closing question

**Q12.1 — "If you had a magic wand for your commercial operations, what's the first thing you'd fix?"**
- *Why:* an unprompted priority; often the truest signal of the day.
- → D1/D2 · H-SEG-AUDIT-01, H-SEG-PROF-01 · `notes`.

---

## 13. Permission to follow up

**Q13.1 — "May we come back to you as this develops, and would you be open to trying an early version?"**
- *Why:* a soft commitment is itself a signal; also enables the pilot that could reach grade A.
- → D3 · H-GTM-GATE-01 · `notes`.

---

## After the interview (interviewer, same day)

1. Fill every covered field in one row of `data/raw/discovery_interviews.csv`.
2. Score `pain_score`, `budget_signal`, `urgency_signal`, `crm_maturity`, `workflow_maturity`,
   `ai_readiness_maturity`, `willingness_to_pay_signal`, `sales_cycle_signal`,
   `evidence_quality_score`, `bias_risk` using
   `templates/discovery_interview_scoring_guide.md` (all 0–100).
3. Set `decision_linked`, `claim_linked`, and `supports_or_refutes` (supports / refutes / mixed /
   neutral) for the **primary** claim the interview bore on. (Secondary claims are captured when you
   create evidence records.)
4. Map the interview into `data/processed/discovery_evidence.csv` — one record per claim — using
   `templates/evidence_capture_template.md`.
