"""Transparent weighted scoring for the Commercial Intelligence Lab.

Every public function returns a score in the closed range ``[0, 100]`` and is safe against missing
inputs (a missing sub-score is treated as the neutral midpoint of its scale rather than crashing).

Weights live in module-level dictionaries so they can be changed, audited, and diffed without
touching logic. They mirror the framework YAML files in ``frameworks/`` — the YAML is the canonical
declaration for humans; these dicts are the canonical values for computation. Keep them in sync (or
drive scoring straight from YAML via ``utils.weights_from_framework``).

A weight spec is ``{criterion_name: {"weight": float, "direction": str}}`` where ``direction`` is
``"higher_better"`` or ``"lower_better"`` (the latter inverts the sub-score, so penalties such as long
sales cycles or high competition reduce the score).
"""

from __future__ import annotations

from typing import Mapping

from .utils import clamp, get_num

# Sub-scores in the sample data are on a 0..10 scale.
INPUT_SCALE = 10.0


# --- Weight specifications (mirror frameworks/*.yml) --------------------------------

MARKET_PRIORITY_WEIGHTS: dict[str, dict] = {
    "market_size_score":      {"weight": 0.20, "direction": "higher_better"},
    "pain_score":             {"weight": 0.22, "direction": "higher_better"},
    "budget_score":           {"weight": 0.16, "direction": "higher_better"},
    "competition_score":      {"weight": 0.12, "direction": "lower_better"},
    "sales_cycle_score":      {"weight": 0.10, "direction": "lower_better"},
    "strategic_fit_score":    {"weight": 0.12, "direction": "higher_better"},
    "evidence_quality_score": {"weight": 0.08, "direction": "higher_better"},
}

CUSTOMER_FIT_WEIGHTS: dict[str, dict] = {
    "current_crm_maturity": {"weight": 0.10, "direction": "lower_better"},
    "workflow_maturity":    {"weight": 0.15, "direction": "higher_better"},
    "data_quality":         {"weight": 0.15, "direction": "higher_better"},
    "budget_signal":        {"weight": 0.20, "direction": "higher_better"},
    "urgency_signal":       {"weight": 0.22, "direction": "higher_better"},
    "decision_complexity":  {"weight": 0.18, "direction": "lower_better"},
}

AI_READINESS_WEIGHTS: dict[str, dict] = {
    "data_quality":         {"weight": 0.28, "direction": "higher_better"},
    "workflow_maturity":    {"weight": 0.18, "direction": "higher_better"},
    "analytics_maturity":   {"weight": 0.22, "direction": "higher_better"},
    "current_crm_maturity": {"weight": 0.12, "direction": "higher_better"},
    "ai_readiness":         {"weight": 0.20, "direction": "higher_better"},
}


# --- Core weighted scorer ----------------------------------------------------------

def weighted_score(
    row: Mapping[str, object],
    weights: Mapping[str, dict],
    input_scale: float = INPUT_SCALE,
) -> float:
    """Compute a 0..100 weighted score from a row of 0..``input_scale`` sub-scores.

    - Missing/invalid sub-scores are treated as the neutral midpoint (no crash, no bias).
    - ``lower_better`` criteria are inverted before weighting.
    - The result is clamped to [0, 100] and rounded to 2 decimals.

    If the provided weights sum to ``W``, the maximum achievable score is ``100 * W``; when weights
    sum to 1.0 (the convention here) the full 0..100 range is available.
    """
    neutral = input_scale / 2.0
    total = 0.0
    for name, spec in weights.items():
        weight = float(spec.get("weight", 0.0))
        direction = spec.get("direction", "higher_better")

        value = get_num(row, name)
        if value is None:
            value = neutral  # missing input -> neutral, keeps the function total-safe

        value = clamp(value, 0.0, input_scale)
        normalised = value / input_scale
        if direction == "lower_better":
            normalised = 1.0 - normalised

        total += normalised * weight

    return round(clamp(total * 100.0, 0.0, 100.0), 2)


# --- Public scoring functions ------------------------------------------------------

def calculate_market_priority_score(row: Mapping[str, object]) -> float:
    """Priority (0..100) of a market segment for first CRM targeting.

    Reads the ``*_score`` columns of ``data/sample/market_segments.csv``. Competition and sales-cycle
    act as penalties (``lower_better``).
    """
    return weighted_score(row, MARKET_PRIORITY_WEIGHTS)


def calculate_customer_fit_score(row: Mapping[str, object]) -> float:
    """Fit (0..100) of an individual customer for the CRM right now.

    Reads maturity/signal columns of ``data/sample/customer_profiles.csv``. Existing CRM maturity and
    decision complexity act as penalties (``lower_better``).
    """
    return weighted_score(row, CUSTOMER_FIT_WEIGHTS)


def calculate_ai_readiness_score(row: Mapping[str, object]) -> float:
    """AI readiness (0..100) of a customer given their CRM/data foundation.

    Operationalises the proposal's core claim that the CRM is the foundation for AI readiness; data
    quality is the most heavily weighted input.
    """
    return weighted_score(row, AI_READINESS_WEIGHTS)
