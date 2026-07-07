"""Tests for the Phase 1 Evidence Operating Layer.

Covers the register schemas, the value validators (grades, supports/refutes, score ranges), and the
integrity of the decision/claim registers — plus a guard that the project stays at v0.1 hypothesis
stage (nothing validated).
"""

import pandas as pd
import pytest

from src.utils import load_sample, load_raw, load_processed
from src.validation import (
    CLAIM_REGISTER_COLUMNS,
    DECISION_REGISTER_COLUMNS,
    DISCOVERY_EVIDENCE_COLUMNS,
    DISCOVERY_INTERVIEW_COLUMNS,
    INTERVIEW_SCORE_COLUMNS,
    validate_claim_register,
    validate_confidence_grades,
    validate_decision_register,
    validate_discovery_evidence,
    validate_discovery_interviews,
    validate_scores_in_range,
    validate_supports_or_refutes,
)


# --- Register schemas load and validate ------------------------------------

def test_decision_register_loads_and_validates():
    df = load_sample("decision_register.csv")
    assert validate_decision_register(df) is True
    assert list(df.columns) == DECISION_REGISTER_COLUMNS
    assert df["decision_id"].is_unique
    assert len(df) == 3


def test_claim_register_loads_and_validates():
    df = load_sample("claim_register.csv")
    assert validate_claim_register(df) is True
    assert list(df.columns) == CLAIM_REGISTER_COLUMNS
    assert df["claim_id"].is_unique
    assert len(df) == 9


def test_discovery_interviews_schema():
    df = load_raw("discovery_interviews.csv")
    assert validate_discovery_interviews(df) is True
    assert list(df.columns) == DISCOVERY_INTERVIEW_COLUMNS


def test_discovery_evidence_schema():
    df = load_processed("discovery_evidence.csv")
    assert validate_discovery_evidence(df) is True
    assert list(df.columns) == DISCOVERY_EVIDENCE_COLUMNS


# --- Referential integrity between registers -------------------------------

def test_claims_reference_real_decisions():
    decisions = set(load_sample("decision_register.csv")["decision_id"])
    claims = load_sample("claim_register.csv")
    assert set(claims["decision_id"]).issubset(decisions)


def test_registers_use_valid_confidence_grades():
    decisions = load_sample("decision_register.csv")
    claims = load_sample("claim_register.csv")
    assert validate_confidence_grades(
        decisions, ["current_confidence_grade", "required_confidence_grade"]) is True
    assert validate_confidence_grades(claims, ["current_confidence_grade"]) is True


# --- v0.1 guard: nothing validated -----------------------------------------

def test_no_claim_is_validated_at_v01():
    """Every claim must remain a hypothesis (grade C or D) — no grade A/B at v0.1."""
    claims = load_sample("claim_register.csv")
    grades = set(claims["current_confidence_grade"].str.upper())
    assert grades.issubset({"C", "D"}), f"unexpected validated grades: {grades}"
    assert (claims["status"].str.lower() == "hypothesis").all()


def test_no_decision_is_validated_at_v01():
    decisions = load_sample("decision_register.csv")
    grades = set(decisions["current_confidence_grade"].str.upper())
    assert "A" not in grades and "B" not in grades


# --- validate_confidence_grades --------------------------------------------

def test_confidence_grades_accepts_valid():
    df = pd.DataFrame({"g": ["A", "B", "C", "D", None]})
    assert validate_confidence_grades(df, ["g"]) is True


@pytest.mark.parametrize("bad", ["E", "X", "1", "AA", "b+"])
def test_confidence_grades_rejects_invalid(bad):
    df = pd.DataFrame({"g": ["A", bad]})
    with pytest.raises(ValueError):
        validate_confidence_grades(df, ["g"])


def test_confidence_grades_missing_column_raises():
    df = pd.DataFrame({"g": ["A"]})
    with pytest.raises(ValueError):
        validate_confidence_grades(df, ["not_here"])


# --- validate_supports_or_refutes ------------------------------------------

def test_supports_or_refutes_accepts_valid():
    df = pd.DataFrame({"supports_or_refutes": ["supports", "refutes", "mixed", "neutral", None]})
    assert validate_supports_or_refutes(df) is True


@pytest.mark.parametrize("bad", ["yes", "no", "maybe", "support"])
def test_supports_or_refutes_rejects_invalid(bad):
    df = pd.DataFrame({"supports_or_refutes": ["supports", bad]})
    with pytest.raises(ValueError):
        validate_supports_or_refutes(df)


def test_supports_or_refutes_empty_frame_ok():
    # header-only / no rows validates vacuously
    df = pd.DataFrame({"supports_or_refutes": pd.Series([], dtype=object)})
    assert validate_supports_or_refutes(df) is True


# --- validate_scores_in_range ----------------------------------------------

def test_scores_in_range_accepts_valid():
    df = pd.DataFrame({"pain_score": [0, 50, 100], "budget_signal": [10.5, 99.9, 0]})
    assert validate_scores_in_range(df, ["pain_score", "budget_signal"]) is True


@pytest.mark.parametrize("bad", [-1, 101, 250, -0.5])
def test_scores_in_range_rejects_out_of_range(bad):
    df = pd.DataFrame({"pain_score": [50, bad]})
    with pytest.raises(ValueError):
        validate_scores_in_range(df, ["pain_score"])


def test_scores_in_range_custom_bounds_for_quality():
    # quality_score is on a 0–1 scale
    ok = pd.DataFrame({"quality_score": [0.0, 0.4, 1.0]})
    assert validate_scores_in_range(ok, ["quality_score"], low=0.0, high=1.0) is True
    bad = pd.DataFrame({"quality_score": [0.4, 1.5]})
    with pytest.raises(ValueError):
        validate_scores_in_range(bad, ["quality_score"], low=0.0, high=1.0)


def test_interview_score_columns_present_in_schema():
    # the 0–100 signal columns must all exist in the interview schema
    assert set(INTERVIEW_SCORE_COLUMNS).issubset(set(DISCOVERY_INTERVIEW_COLUMNS))
