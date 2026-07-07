# Positioning Message Test — First Evidence Sprint

A short, structured test embedded in the discovery interview (Section 11 of
`templates/discovery_interview_script.md`). It tests **Decision 2 · Positioning** against real buyers
in the audit and professional-services segments.

**What it feeds:** `positioning_preference` in `data/raw/discovery_interviews.csv`
(`CRM` / `RevOps` / `AI Readiness` / `unclear`), plus `notes`. Claims informed: **H-POS-CRM-01**,
**H-POS-REVOPS-01**, **H-POS-AI-01** (and, on the AI framing, **H-AI-READY-01/02**).

---

## How to administer

1. Read all three one-line descriptions in a **randomised order** (rotate first position across
   interviews to reduce order bias — note the order in `notes`).
2. Ask: *"Which of these sounds most like something your firm needs — and why?"*
3. Then ask: *"Is anything here overpromised or not credible?"*
4. Record the chosen framing in `positioning_preference` and the reasoning verbatim in `notes`.
5. Do **not** editorialise or defend a framing — you are measuring reaction, not selling.

> **Bias control.** Never reveal which framing is "ours". If the respondent asks, say all three are
> under consideration. Leading here corrupts the single most important D2 signal — reflect any leading
> in a higher `bias_risk` score.

---

## Option 1 — CRM Platform

**Short description (read aloud):**
> "A system of record for your clients and pipeline — contacts, deals, and activity in one place, so
> nothing falls through the cracks."

- **What we are testing:** whether "CRM" is instantly understood but perceived as generic /
  commoditised.
- **Interpretation:** high comprehension + low excitement = *clear but generic*. If chosen mainly
  because it's familiar (not because it's compelling), that **supports H-POS-CRM-01**. Genuine
  enthusiasm would **refute** it.
- **Informs claim:** **H-POS-CRM-01** — "CRM positioning may be clear but too generic."

## Option 2 — Revenue Operations Platform

**Short description (read aloud):**
> "A platform that connects your commercial workflow end-to-end — pipeline, delivery, and the handoffs
> between them — so you can see and improve how revenue actually gets made."

- **What we are testing:** whether a RevOps framing expresses business value better than "CRM" without
  losing clarity.
- **Interpretation:** preference for this framing *because it maps to a felt operational problem*
  **supports H-POS-REVOPS-01**. Confusion about what it means (needs explaining) is a caution — note
  it. Watch for respondents who like the words but can't say what it does.
- **Informs claim:** **H-POS-REVOPS-01** — "Revenue Operations Platform positioning may better express
  business value."

## Option 3 — AI Readiness Platform

**Short description (read aloud):**
> "A platform that gets your client and commercial data structured and clean, so your firm is ready to
> use AI to work faster and smarter."

- **What we are testing:** whether the AI framing is differentiated and exciting **or** overpromising
  and not credible for this buyer today.
- **Interpretation:** excitement + belief = differentiated (note it). Excitement + scepticism
  ("sounds like hype", "we're nowhere near that") **supports H-POS-AI-01** (differentiated but may
  overpromise). Reasoning about their own data readiness also informs **H-AI-READY-01/02** — capture
  it.
- **Informs claim:** **H-POS-AI-01** — "AI Readiness Platform positioning may be differentiated but
  could overpromise." (Secondary: H-AI-READY-01, H-AI-READY-02.)

---

## Recording the result

| Observation | `positioning_preference` | Also note in `notes` |
|---|---|---|
| Clear single preference | `CRM` / `RevOps` / `AI Readiness` | the *reason*, verbatim |
| Likes two roughly equally | the stronger one | the trade-off they described |
| No clear preference / confused | `unclear` | what confused them |

Then, when creating evidence records (`templates/evidence_capture_template.md`), write **one record
per positioning claim the answer bears on**, each with `supports` / `refutes` / `mixed` / `neutral`
and a one-line `evidence_summary`.

---

## What this test cannot do (yet)

- It is **comprehension + stated preference**, not behaviour. A stated preference is weaker than a
  won deal. Treat results as grade-C signal at best until corroborated across many interviews.
- It does not price the offering — willingness-to-pay is probed separately (script Q11.3).
- **Do not** conclude a positioning from the sprint. The gate for D2 is grade **B** across converging
  message tests; a handful of interviews cannot clear it.
