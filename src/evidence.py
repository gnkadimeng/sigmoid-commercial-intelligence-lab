"""Evidence weighting, strength classification, and aggregation (CIS §10).

Evidence is the currency of the system. This module implements the operational rules:

- an item's **weight** discounts its raw quality by its bias risk;
- an item **supports**, **refutes**, or gives **mixed** signal on a claim;
- a claim's **strength of support** is a classification derived from the net weight of its evidence.

Everything is pure and testable against known inputs.
"""

from __future__ import annotations

from typing import Mapping

from .utils import get_str, to_float

# Bias risk discounts the usable weight of an otherwise-good source.
BIAS_ADJUSTMENT: dict[str, float] = {"low": 1.0, "medium": 0.7, "high": 0.4}

# Direction an item pushes a claim.
SUPPORT_SIGN: dict[str, float] = {"yes": 1.0, "no": -1.0, "mixed": 0.0}

# Net-weight thresholds for classifying strength of support for a claim.
STRENGTH_THRESHOLDS = (
    (0.5, "weak"),      # 0 <  net < 0.5
    (1.2, "moderate"),  # 0.5 <= net < 1.2
)                        # net >= 1.2 -> "strong"; net <= 0 -> "none"


def calculate_evidence_weight(row: Mapping[str, object]) -> float:
    """Weight (0..1) of a single evidence item = quality_score x bias adjustment.

    ``quality_score`` is clamped to [0, 1]; unknown/blank quality is treated as 0. Unknown bias risk
    is treated as high (the conservative choice). Rounded to 4 decimals.
    """
    quality = to_float(row_get(row, "quality_score"))
    if quality is None:
        quality = 0.0
    quality = max(0.0, min(1.0, quality))

    bias = get_str(row, "bias_risk", "high")
    adjustment = BIAS_ADJUSTMENT.get(bias, BIAS_ADJUSTMENT["high"])

    return round(quality * adjustment, 4)


def classify_evidence_strength(score: float) -> str:
    """Classify a claim's net evidence weight into none/weak/moderate/strong.

    ``score`` is the *net* supporting weight (supporting minus refuting). Non-positive net support is
    ``"none"`` — a refuted or unsupported claim has no strength of support.
    """
    value = to_float(score)
    if value is None or value <= 0.0:
        return "none"
    for threshold, label in STRENGTH_THRESHOLDS:
        if value < threshold:
            return label
    return "strong"


def summarise_evidence_by_claim(df):
    """Aggregate an evidence register into one row per claim.

    Returns a DataFrame with columns:
    ``claim_id, n_evidence, total_weight, supporting_weight, refuting_weight, net_weight, strength``
    sorted by net_weight (strongest support first). ``supports_claim`` values map to signs
    (yes=+1, no=-1, mixed=0); net_weight drives the strength classification.
    """
    import pandas as pd

    records = []
    for claim_id, group in df.groupby("claim_id"):
        weights = group.apply(calculate_evidence_weight, axis=1)
        signs = (
            group["supports_claim"].map(lambda v: SUPPORT_SIGN.get(str(v).strip().lower(), 0.0))
        )
        signed = weights * signs
        supporting = float(weights[signs > 0].sum())
        refuting = float(weights[signs < 0].sum())
        net = float(signed.sum())
        records.append(
            {
                "claim_id": claim_id,
                "n_evidence": int(len(group)),
                "total_weight": round(float(weights.sum()), 4),
                "supporting_weight": round(supporting, 4),
                "refuting_weight": round(refuting, 4),
                "net_weight": round(net, 4),
                "strength": classify_evidence_strength(net),
            }
        )

    result = pd.DataFrame(
        records,
        columns=[
            "claim_id",
            "n_evidence",
            "total_weight",
            "supporting_weight",
            "refuting_weight",
            "net_weight",
            "strength",
        ],
    )
    if not result.empty:
        result = result.sort_values("net_weight", ascending=False).reset_index(drop=True)
    return result


def row_get(row: Mapping[str, object], key: str):
    """Small helper: fetch a raw value from a dict or pandas row, tolerating missing keys."""
    try:
        return row[key]
    except (KeyError, IndexError, TypeError):
        return None
