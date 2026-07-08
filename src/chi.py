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


# Confidence grade ordering (CIS): D (worst) < C < B < A (best).
GRADE_RANK = {"D": 0, "C": 1, "B": 2, "A": 3}
RANK_GRADE = {v: k for k, v in GRADE_RANK.items()}


def load_measured(business_id: str | None = None,
                  name: str = "commercial_health_measured.csv") -> dict:
    """Load measured dimension scores for a business from data/sample/<name>.

    Returns ``{dimension_id: {"score": float, "confidence": "B"|"A", "source": str}}``. The file is a
    template (header-only) until real data is collected — an empty file yields ``{}``, so the index
    stays self-assessed (grade C). Never invents data.
    """
    from .utils import load_sample

    try:
        df = load_sample(name)
    except Exception:
        return {}
    if df.empty:
        return {}
    if business_id is not None and "business_id" in df.columns:
        df = df[df["business_id"] == business_id]
    out: dict = {}
    for _, row in df.iterrows():
        did = str(row.get("dimension_id", "")).strip()
        score = to_float(row.get("score"))
        if not did or score is None:
            continue
        out[did] = {
            "score": clamp(score, 0.0, 100.0),
            "confidence": str(row.get("confidence", "B")).strip().upper() or "B",
            "source": row.get("source", ""),
        }
    return out


def commercial_health_index(responses: Mapping[str, Sequence],
                            framework: dict | None = None,
                            measured: Mapping[str, dict] | None = None) -> dict:
    """Compute the Commercial Health Index.

    ``responses`` maps a dimension id (e.g. ``"D1"``) to its list of 1..5 self-assessment answers.
    ``measured`` optionally maps a dimension id to a measured score
    (``{"score": 0..100, "confidence": "B"|"A", "source": str}``) — where present it **overrides**
    self-report for that dimension and carries its higher confidence.

    Overall confidence is the **lowest** grade among the dimensions that drive the index (CIS §8): a
    single self-assessed dimension caps the whole index at grade C. Partial input is handled; a
    dimension with neither measured nor self-assessed input is left unscored.
    """
    fw = framework or load_chi()
    measured = measured or {}
    self_grade = fw.get("confidence_self_report", "C")

    dims_out = []
    weighted_sum = 0.0
    weight_total = 0.0
    grades = []

    for dim in fw["dimensions"]:
        did = dim["id"]
        weight = float(dim.get("weight", 0.0))
        score, mode, grade = None, None, None

        m = measured.get(did)
        if m is not None:
            ms = to_float(m.get("score") if isinstance(m, dict) else m)
            if ms is not None:
                score = round(clamp(ms, 0.0, 100.0), 1)
                mode = "measured"
                grade = (m.get("confidence") if isinstance(m, dict) else None) or "B"
                grade = grade if grade in GRADE_RANK else "B"

        if score is None:
            score = score_dimension(responses.get(did) if responses else None)
            if score is not None:
                mode, grade = "self", self_grade

        dims_out.append({
            "id": did,
            "name": dim["name"],
            "weight": weight,
            "score": score,
            "mode": mode,
            "confidence": grade,
            "next_move": dim.get("next_move", ""),
        })
        if score is not None:
            weighted_sum += weight * score
            weight_total += weight
            grades.append(grade)

    chi = round(weighted_sum / weight_total, 1) if weight_total > 0 else None
    band = interpret_band(chi, fw["bands"]) if chi is not None else None
    confidence = RANK_GRADE[min(GRADE_RANK.get(g, 1) for g in grades)] if grades else None

    scored = [d for d in dims_out if d["score"] is not None]
    gaps = sorted(scored, key=lambda d: d["score"])[:2]

    return {
        "chi": chi,
        "band": band,
        "confidence": confidence,
        "dimensions": dims_out,
        "gaps": gaps,
    }
