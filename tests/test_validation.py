"""Tests for src.validation — range predicate, required columns, negative-score guard."""

import pandas as pd
import pytest

from src.validation import (
    validate_no_negative_scores,
    validate_required_columns,
    validate_score_range,
)


# --- validate_score_range ----------------------------------------------------------

@pytest.mark.parametrize("value", [0, 50, 100, 99.99, "0", "100"])
def test_score_range_accepts_valid(value):
    assert validate_score_range(value) is True


@pytest.mark.parametrize("value", [-1, 101, 150, -0.01, "abc", None, float("nan")])
def test_score_range_rejects_invalid(value):
    assert validate_score_range(value) is False


def test_score_range_custom_bounds():
    assert validate_score_range(0.8, low=0.0, high=1.0) is True
    assert validate_score_range(1.5, low=0.0, high=1.0) is False


# --- validate_required_columns -----------------------------------------------------

def test_required_columns_pass():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    assert validate_required_columns(df, ["a", "b"]) is True


def test_required_columns_missing_raises():
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(ValueError) as exc:
        validate_required_columns(df, ["a", "b", "z"])
    assert "b" in str(exc.value) and "z" in str(exc.value)


# --- validate_no_negative_scores ---------------------------------------------------

def test_no_negative_scores_pass():
    df = pd.DataFrame({"x": [0, 5, 10], "y": [1.0, 2.5, 3.0]})
    assert validate_no_negative_scores(df, ["x", "y"]) is True


def test_negative_scores_are_caught():
    df = pd.DataFrame({"x": [0, -3, 10]})
    with pytest.raises(ValueError) as exc:
        validate_no_negative_scores(df, ["x"])
    assert "x" in str(exc.value)


def test_missing_score_column_raises():
    df = pd.DataFrame({"x": [1, 2, 3]})
    with pytest.raises(ValueError):
        validate_no_negative_scores(df, ["x", "not_here"])
