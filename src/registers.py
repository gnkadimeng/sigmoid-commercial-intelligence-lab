"""Evidence Operating Layer — register queries and lightweight HTML views.

Loads the decision and claim registers plus the processed discovery evidence, and provides small
helpers the ``.qmd`` pages use to render decisions and claims **directly from the data** (single
source of truth). Real discovery evidence starts empty, so the helpers degrade gracefully to the
"hypothesis stage" — showing what evidence is still needed rather than inventing any.

HTML links are emitted with explicit ``.html`` targets and a ``rel`` prefix because raw-HTML links are
not rewritten by Quarto the way markdown links are. Pages under a single subdirectory (``decisions/``,
``evidence/``) use ``rel="../"``.
"""

from __future__ import annotations

import html

from .utils import load_processed, load_sample

CONF_CHIP = {"A": "chip-grade-a", "B": "chip-grade-b", "C": "chip-grade-c", "D": "chip-grade-d"}

FRAMEWORK_NAMES = {
    "market_prioritisation": "Market Prioritisation",
    "customer_fit_score": "Customer Fit Score",
    "ai_readiness_index": "AI Readiness Index",
    "positioning_canvas": "Positioning Canvas",
    "pricing_model": "Pricing Model",
}
DASHBOARD_NAMES = {
    "market-prioritisation": "Market Prioritisation",
    "ai-readiness-scorecard": "AI Readiness Scorecard",
    "positioning-dashboard": "Positioning Dashboard",
}


# --- Loaders ----------------------------------------------------------------

def load_decision_register():
    return load_sample("decision_register.csv")


def load_claim_register():
    return load_sample("claim_register.csv")


def load_discovery_evidence():
    return load_processed("discovery_evidence.csv")


# --- Queries ----------------------------------------------------------------

def get_decision(decision_id: str):
    df = load_decision_register()
    rows = df[df["decision_id"] == decision_id]
    if rows.empty:
        raise KeyError(f"Unknown decision_id: {decision_id}")
    return rows.iloc[0]


def claims_for_decision(decision_id: str):
    df = load_claim_register()
    return df[df["decision_id"] == decision_id].copy()


def evidence_for_claim(claim_id: str):
    ev = load_discovery_evidence()
    if ev.empty or "claim_id" not in ev.columns:
        return ev
    return ev[ev["claim_id"] == claim_id].copy()


def claim_evidence_counts(claim_id: str) -> dict:
    """Real discovery-evidence counts for a claim: supports / refutes / mixed / neutral / total."""
    out = {"supports": 0, "refutes": 0, "mixed": 0, "neutral": 0, "total": 0}
    ev = evidence_for_claim(claim_id)
    if not ev.empty and "supports_or_refutes" in ev.columns:
        vc = ev["supports_or_refutes"].astype(str).str.strip().str.lower().value_counts()
        for key in ("supports", "refutes", "mixed", "neutral"):
            out[key] = int(vc.get(key, 0))
        out["total"] = int(len(ev))
    return out


# --- View helpers (return HTML strings for IPython.display.HTML) ------------

def _esc(x) -> str:
    return html.escape("" if x is None else str(x))


def _grade_chip(grade) -> str:
    g = str(grade).strip().upper()
    return f'<span class="chip {CONF_CHIP.get(g, "chip-neutral")}">{_esc(g)}</span>'


def _split_multi(value) -> list[str]:
    """Split a ';'-separated register cell into a clean list."""
    if value is None:
        return []
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def _framework_links(value, rel: str) -> str:
    items = _split_multi(value)
    if not items:
        return "—"
    return ", ".join(
        f'<a href="{rel}frameworks/index.html">{_esc(FRAMEWORK_NAMES.get(i, i))}</a>' for i in items
    )


def _dashboard_links(value, rel: str) -> str:
    items = _split_multi(value)
    if not items:
        return "—"
    return ", ".join(
        f'<a href="{rel}dashboards/{i}.html">{_esc(DASHBOARD_NAMES.get(i, i))}</a>' for i in items
    )


def render_decision_record(decision_id: str, rel: str = "../") -> str:
    """Render a decision's register row as the question/hypothesis panel + a fields grid."""
    d = get_decision(decision_id)
    grade = _grade_chip(d["current_confidence_grade"])
    required = _grade_chip(d["required_confidence_grade"])

    thesis = (
        '<div class="wp-thesis">'
        '<div class="wp-t-cell"><div class="wp-t-label">Decision question</div>'
        f'<p>{_esc(d["decision_question"])}</p></div>'
        '<div class="wp-t-cell"><div class="wp-t-label">Current hypothesis · '
        f'grade {_esc(d["current_confidence_grade"])}</div>'
        f'<p>{_esc(d["current_hypothesis"])}</p></div>'
        '</div>'
    )

    def cell(label, val):
        return (f'<div class="pg-cell"><div class="pg-label">{_esc(label)}</div>'
                f'<div class="pg-val">{val}</div></div>')

    grid = (
        '<div class="purpose-grid">'
        + cell("Status", _esc(d["current_status"]))
        + cell("Confidence", f'{grade} <span class="text-muted-sig">→ requires</span> {required}')
        + cell("Frameworks used", _framework_links(d["linked_frameworks"], rel))
        + cell("Dashboards linked", _dashboard_links(d["linked_dashboards"], rel))
        + cell("Next experiment", _esc(d["next_experiment"]))
        + cell("Owner · last reviewed", f'{_esc(d["owner"])} · {_esc(d["last_reviewed"])}')
        + '</div>'
    )
    return thesis + grid


def render_claim_cards(decision_id: str, rel: str = "../") -> str:
    """Render the claims for a decision as cards, with what evidence each still needs."""
    claims = claims_for_decision(decision_id)
    cards = []
    for _, c in claims.iterrows():
        counts = claim_evidence_counts(c["claim_id"])
        if counts["total"] == 0:
            evidence_state = ('<span class="text-muted-sig">No real evidence yet — hypothesis. '
                              'Awaiting discovery interviews.</span>')
        else:
            evidence_state = (f'{counts["supports"]} support · {counts["refutes"]} refute · '
                              f'{counts["mixed"]} mixed · {counts["neutral"]} neutral '
                              f'({counts["total"]} items)')
        cards.append(
            '<div class="framework-card">'
            '<div class="fc-head">'
            f'<p class="fc-title">{_esc(c["claim_id"])}</p>'
            f'{_grade_chip(c["current_confidence_grade"])}'
            f'<span class="chip chip-neutral no-dot">{_esc(c["claim_type"])}</span>'
            f'<p class="fc-q">{_esc(c["claim_text"])}</p>'
            '</div>'
            '<div class="fc-body">'
            f'<div class="fc-field"><div class="fc-label">Real evidence</div>'
            f'<div class="fc-val">{evidence_state}</div></div>'
            f'<div class="fc-field"><div class="fc-label">Needed for grade B</div>'
            f'<div class="fc-val">{_esc(c["evidence_needed_for_B"])}</div></div>'
            f'<div class="fc-field"><div class="fc-label">Needed for grade A</div>'
            f'<div class="fc-val">{_esc(c["evidence_needed_for_A"])}</div></div>'
            '</div>'
            '</div>'
        )
    return '<div class="framework-grid">' + "".join(cards) + "</div>"
