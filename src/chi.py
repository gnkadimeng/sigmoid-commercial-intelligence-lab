"""Commercial Health Index (CHI) — reference scorer.

Implements the Commercial Health Index Specification (CHI-S v0.1): seven dimensions, each with three
self-assessed statements rated 1..5, scored to 0..100, combined into a weighted overall index, and
interpreted against the SCS maturity ladder. Every score carries a confidence grade (self-assessment
mode is capped at C).

Weights, statements, and bands live in ``frameworks/commercial_health_index.yml`` — this module is the
logic, the YAML is the data.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from .utils import FRAMEWORKS_DIR, clamp, to_float


def load_chi() -> dict:
    """Load the CHI framework definition from YAML."""
    import yaml

    with (FRAMEWORKS_DIR / "commercial_health_index.yml").open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def answer_to_100(answer, low: float = 1.0, high: float = 5.0) -> float | None:
    """Map a 1..5 answer to a 0..100 score. Missing/invalid answers return None."""
    value = to_float(answer)
    if value is None:
        return None
    value = clamp(value, low, high)
    return (value - low) / (high - low) * 100.0


def score_dimension(answers: Sequence) -> float | None:
    """Mean 0..100 score for a dimension's answers. None if no valid answers."""
    scores = [answer_to_100(a) for a in (answers or [])]
    scores = [s for s in scores if s is not None]
    if not scores:
        return None
    return round(sum(scores) / len(scores), 1)


def interpret_band(score, bands: Sequence[Mapping]) -> dict | None:
    """Return the band a 0..100 score falls into."""
    value = to_float(score)
    if value is None:
        return None
    value = clamp(value, 0.0, 100.0)
    for band in bands:
        if band["min"] <= value <= band["max"]:
            return dict(band)
    return dict(bands[-1])


def commercial_health_index(responses: Mapping[str, Sequence], framework: dict | None = None) -> dict:
    """Compute the Commercial Health Index from self-assessment responses.

    ``responses`` maps a dimension id (e.g. ``"D1"``) to its list of 1..5 answers. Partial input is
    handled: a dimension with no valid answers is left unscored and excluded from the index.

    Returns a dict with the overall ``chi`` (0..100 or None), its ``band``, the ``confidence`` grade,
    the per-``dimensions`` breakdown, and the lowest-scoring ``gaps``.
    """
    fw = framework or load_chi()
    dims_out = []
    weighted_sum = 0.0
    weight_total = 0.0

    for dim in fw["dimensions"]:
        score = score_dimension(responses.get(dim["id"]) if responses else None)
        dims_out.append({
            "id": dim["id"],
            "name": dim["name"],
            "weight": float(dim.get("weight", 0.0)),
            "score": score,
            "next_move": dim.get("next_move", ""),
        })
        if score is not None:
            weighted_sum += float(dim.get("weight", 0.0)) * score
            weight_total += float(dim.get("weight", 0.0))

    chi = round(weighted_sum / weight_total, 1) if weight_total > 0 else None
    band = interpret_band(chi, fw["bands"]) if chi is not None else None

    scored = [d for d in dims_out if d["score"] is not None]
    gaps = sorted(scored, key=lambda d: d["score"])[:2]

    return {
        "chi": chi,
        "band": band,
        "confidence": fw.get("confidence_self_report", "C"),
        "dimensions": dims_out,
        "gaps": gaps,
    }
