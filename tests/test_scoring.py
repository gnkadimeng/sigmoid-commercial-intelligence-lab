"""Tests for src.scoring — range guarantees and missing-value safety."""

import pytest

from src.scoring import (
    calculate_ai_readiness_score,
    calculate_customer_fit_score,
    calculate_market_priority_score,
)

# A representative full row for each scorer (0..10 sub-scores).
MARKET_ROW = {
    "market_size_score": 8,
    "pain_score": 9,
    "budget_score": 7,
    "competition_score": 3,
    "sales_cycle_score": 2,
    "strategic_fit_score": 8,
    "evidence_quality_score": 5,
}

CUSTOMER_ROW = {
    "current_crm_maturity": 2,
    "workflow_maturity": 7,
    "data_quality": 7,
    "budget_signal": 8,
    "urgency_signal": 8,
    "decision_complexity": 3,
}

AI_ROW = {
    "data_quality": 8,
    "workflow_maturity": 7,
    "analytics_maturity": 7,
    "current_crm_maturity": 5,
    "ai_readiness": 7,
}

ALL_SCORERS = [
    (calculate_market_priority_score, MARKET_ROW),
    (calculate_customer_fit_score, CUSTOMER_ROW),
    (calculate_ai_readiness_score, AI_ROW),
]


@pytest.mark.parametrize("scorer,row", ALL_SCORERS)
def test_scores_within_0_100(scorer, row):
    score = scorer(row)
    assert 0.0 <= score <= 100.0


def test_market_priority_score_in_range():
    assert 0.0 <= calculate_market_priority_score(MARKET_ROW) <= 100.0


def test_customer_fit_score_in_range():
    assert 0.0 <= calculate_customer_fit_score(CUSTOMER_ROW) <= 100.0


def test_ai_readiness_score_in_range():
    assert 0.0 <= calculate_ai_readiness_score(AI_ROW) <= 100.0


@pytest.mark.parametrize("scorer,row", ALL_SCORERS)
def test_missing_values_do_not_crash(scorer, row):
    # Drop every key one at a time and also test a fully empty row.
    for key in list(row):
        partial = {k: v for k, v in row.items() if k != key}
        score = scorer(partial)
        assert 0.0 <= score <= 100.0
    empty_score = scorer({})
    assert 0.0 <= empty_score <= 100.0


@pytest.mark.parametrize("scorer", [s for s, _ in ALL_SCORERS])
def test_none_and_bad_values_are_safe(scorer):
    row = {"data_quality": None, "pain_score": "n/a", "urgency_signal": float("nan")}
    score = scorer(row)
    assert 0.0 <= score <= 100.0


def test_higher_pain_raises_market_priority():
    low = {**MARKET_ROW, "pain_score": 1}
    high = {**MARKET_ROW, "pain_score": 10}
    assert calculate_market_priority_score(high) > calculate_market_priority_score(low)


def test_lower_better_criterion_inverts():
    # Higher competition (a penalty) should reduce the market priority score.
    low_comp = {**MARKET_ROW, "competition_score": 1}
    high_comp = {**MARKET_ROW, "competition_score": 10}
    assert calculate_market_priority_score(low_comp) > calculate_market_priority_score(high_comp)
