"""Tests for src.evidence — weighting, strength classification, and per-claim aggregation."""

import pandas as pd

from src.evidence import (
    calculate_evidence_weight,
    classify_evidence_strength,
    summarise_evidence_by_claim,
)


# --- calculate_evidence_weight -----------------------------------------------------

def test_weight_low_bias_full_quality():
    row = {"quality_score": 1.0, "bias_risk": "low"}
    assert calculate_evidence_weight(row) == 1.0


def test_bias_discounts_weight():
    high = calculate_evidence_weight({"quality_score": 0.8, "bias_risk": "low"})
    med = calculate_evidence_weight({"quality_score": 0.8, "bias_risk": "medium"})
    low = calculate_evidence_weight({"quality_score": 0.8, "bias_risk": "high"})
    assert high > med > low


def test_weight_handles_missing_quality():
    # Missing quality -> 0 weight, never a crash.
    assert calculate_evidence_weight({"bias_risk": "low"}) == 0.0


def test_weight_unknown_bias_treated_as_high():
    unknown = calculate_evidence_weight({"quality_score": 1.0, "bias_risk": "???"})
    high = calculate_evidence_weight({"quality_score": 1.0, "bias_risk": "high"})
    assert unknown == high


# --- classify_evidence_strength ----------------------------------------------------

def test_strength_classification_bands():
    assert classify_evidence_strength(0.0) == "none"
    assert classify_evidence_strength(-0.5) == "none"
    assert classify_evidence_strength(0.3) == "weak"
    assert classify_evidence_strength(0.8) == "moderate"
    assert classify_evidence_strength(2.0) == "strong"


def test_strength_is_monotonic():
    order = ["none", "weak", "moderate", "strong"]
    grades = [classify_evidence_strength(x) for x in [0.0, 0.3, 0.8, 2.0]]
    assert grades == order


# --- summarise_evidence_by_claim ---------------------------------------------------

def _register():
    return pd.DataFrame(
        [
            {"evidence_id": "E1", "claim_id": "C1", "quality_score": 1.0, "bias_risk": "low",    "supports_claim": "yes"},
            {"evidence_id": "E2", "claim_id": "C1", "quality_score": 0.5, "bias_risk": "medium", "supports_claim": "yes"},
            {"evidence_id": "E3", "claim_id": "C2", "quality_score": 0.8, "bias_risk": "low",    "supports_claim": "no"},
            {"evidence_id": "E4", "claim_id": "C2", "quality_score": 0.4, "bias_risk": "high",   "supports_claim": "yes"},
        ]
    )


def test_summary_groups_by_claim():
    summary = summarise_evidence_by_claim(_register())
    assert set(summary["claim_id"]) == {"C1", "C2"}
    assert len(summary) == 2
    # Each claim's n_evidence reflects its group size.
    counts = dict(zip(summary["claim_id"], summary["n_evidence"]))
    assert counts["C1"] == 2 and counts["C2"] == 2


def test_summary_net_weight_and_strength():
    summary = summarise_evidence_by_claim(_register()).set_index("claim_id")
    # C1: 1.0 + 0.35 supporting = 1.35 net -> strong.
    assert summary.loc["C1", "net_weight"] > 0
    assert summary.loc["C1", "strength"] == "strong"
    # C2: refuting (0.8) outweighs supporting (0.16) -> negative net -> none.
    assert summary.loc["C2", "net_weight"] < 0
    assert summary.loc["C2", "strength"] == "none"


def test_summary_sorted_by_net_weight_desc():
    summary = summarise_evidence_by_claim(_register())
    net = list(summary["net_weight"])
    assert net == sorted(net, reverse=True)


def test_summary_empty_input():
    empty = pd.DataFrame(columns=["claim_id", "quality_score", "bias_risk", "supports_claim"])
    result = summarise_evidence_by_claim(empty)
    assert result.empty
