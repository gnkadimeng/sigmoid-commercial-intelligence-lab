"""Tests that the synthetic sample datasets load and satisfy their schema/integrity rules."""

import pandas as pd
import pytest

from src.scoring import (
    calculate_ai_readiness_score,
    calculate_customer_fit_score,
    calculate_market_priority_score,
)
from src.utils import load_sample
from src.validation import validate_required_columns, validate_score_range

MARKET_COLUMNS = [
    "segment_id", "segment_name", "industry",
    "market_size_score", "pain_score", "budget_score", "competition_score",
    "sales_cycle_score", "strategic_fit_score", "evidence_quality_score",
]
CUSTOMER_COLUMNS = [
    "customer_id", "company_name", "industry", "employee_band",
    "current_crm_maturity", "workflow_maturity", "data_quality", "analytics_maturity",
    "ai_readiness", "budget_signal", "urgency_signal", "decision_complexity",
]
EVIDENCE_COLUMNS = [
    "evidence_id", "claim_id", "source_type", "source_name",
    "date_collected", "quality_score", "bias_risk", "supports_claim", "notes",
]


# --- Loading -----------------------------------------------------------------------

def test_sample_files_load():
    assert not load_sample("market_segments.csv").empty
    assert not load_sample("customer_profiles.csv").empty
    assert not load_sample("evidence_register.csv").empty


# --- Required columns --------------------------------------------------------------

def test_market_segments_columns():
    df = load_sample("market_segments.csv")
    assert validate_required_columns(df, MARKET_COLUMNS) is True


def test_customer_profiles_columns():
    df = load_sample("customer_profiles.csv")
    assert validate_required_columns(df, CUSTOMER_COLUMNS) is True


def test_evidence_register_columns():
    df = load_sample("evidence_register.csv")
    assert validate_required_columns(df, EVIDENCE_COLUMNS) is True


# --- Identity uniqueness -----------------------------------------------------------

@pytest.mark.parametrize(
    "filename,id_col",
    [
        ("market_segments.csv", "segment_id"),
        ("customer_profiles.csv", "customer_id"),
        ("evidence_register.csv", "evidence_id"),
    ],
)
def test_identity_columns_unique(filename, id_col):
    df = load_sample(filename)
    assert df[id_col].is_unique


# --- Score/metadata ranges ---------------------------------------------------------

def test_evidence_quality_in_unit_range():
    df = load_sample("evidence_register.csv")
    assert df["quality_score"].between(0.0, 1.0).all()


def test_evidence_metadata_values_valid():
    df = load_sample("evidence_register.csv")
    assert df["bias_risk"].str.lower().isin({"low", "medium", "high"}).all()
    assert df["supports_claim"].str.lower().isin({"yes", "no", "mixed"}).all()


def test_computed_scores_on_sample_within_range():
    segments = load_sample("market_segments.csv")
    customers = load_sample("customer_profiles.csv")

    for _, row in segments.iterrows():
        assert validate_score_range(calculate_market_priority_score(row))
    for _, row in customers.iterrows():
        assert validate_score_range(calculate_customer_fit_score(row))
        assert validate_score_range(calculate_ai_readiness_score(row))
