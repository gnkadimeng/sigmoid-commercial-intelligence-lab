"""Tests for the Commercial Health Index scorer (src.chi)."""

import pytest

from src.chi import (
    answer_to_100,
    commercial_health_index,
    interpret_band,
    load_chi,
    score_dimension,
)

FW = load_chi()
DIM_IDS = [d["id"] for d in FW["dimensions"]]


def all_answers(value):
    """Responses dict with every statement answered `value`."""
    return {d["id"]: [value] * len(d["statements"]) for d in FW["dimensions"]}


# --- framework shape --------------------------------------------------------

def test_framework_has_seven_dimensions_with_three_statements():
    assert len(FW["dimensions"]) == 7
    for d in FW["dimensions"]:
        assert len(d["statements"]) == 3
        assert d["next_move"]


def test_weights_sum_to_one():
    total = sum(float(d["weight"]) for d in FW["dimensions"])
    assert total == pytest.approx(1.0, abs=0.01)


def test_five_bands_cover_zero_to_hundred():
    bands = FW["bands"]
    assert len(bands) == 5
    assert bands[0]["min"] == 0 and bands[-1]["max"] == 100


# --- answer_to_100 ----------------------------------------------------------

@pytest.mark.parametrize("ans,expected", [(1, 0), (2, 25), (3, 50), (4, 75), (5, 100)])
def test_answer_maps_to_0_100(ans, expected):
    assert answer_to_100(ans) == expected


@pytest.mark.parametrize("bad", [None, "", "n/a", float("nan")])
def test_answer_missing_is_none(bad):
    assert answer_to_100(bad) is None


def test_answer_out_of_range_clamped():
    assert answer_to_100(0) == 0
    assert answer_to_100(7) == 100


# --- score_dimension --------------------------------------------------------

def test_dimension_all_top_is_100():
    assert score_dimension([5, 5, 5]) == 100


def test_dimension_all_bottom_is_0():
    assert score_dimension([1, 1, 1]) == 0


def test_dimension_mixed():
    assert score_dimension([5, 3, 1]) == 50  # (100 + 50 + 0)/3


def test_dimension_missing_values_safe():
    assert 0 <= score_dimension([5, None, 3]) <= 100
    assert score_dimension([]) is None
    assert score_dimension([None, None]) is None


# --- interpret_band ---------------------------------------------------------

@pytest.mark.parametrize("score,level", [(0, 1), (20, 1), (21, 2), (50, 3), (75, 4), (100, 5)])
def test_band_boundaries(score, level):
    assert interpret_band(score, FW["bands"])["level"] == level


# --- commercial_health_index ------------------------------------------------

def test_chi_all_top_is_100_level_5():
    r = commercial_health_index(all_answers(5), FW)
    assert r["chi"] == 100
    assert r["band"]["level"] == 5
    assert r["confidence"] == "C"          # self-report is capped at grade C
    assert len(r["dimensions"]) == 7


def test_chi_all_bottom_is_0_level_1():
    r = commercial_health_index(all_answers(1), FW)
    assert r["chi"] == 0
    assert r["band"]["level"] == 1


def test_chi_neutral_is_50():
    r = commercial_health_index(all_answers(3), FW)
    assert r["chi"] == pytest.approx(50, abs=0.5)


def test_chi_in_range_and_deterministic():
    r1 = commercial_health_index(all_answers(4), FW)
    r2 = commercial_health_index(all_answers(4), FW)
    assert 0 <= r1["chi"] <= 100
    assert r1 == r2


def test_chi_partial_input_excludes_unscored_dimension():
    r = all_answers(5)
    r.pop("D4")                              # leave one dimension unanswered
    result = commercial_health_index(r, FW)
    d4 = next(d for d in result["dimensions"] if d["id"] == "D4")
    assert d4["score"] is None
    assert result["chi"] == 100              # remaining dims still 100
    assert result["band"]["level"] == 5


def test_chi_gaps_are_lowest_dimensions():
    responses = all_answers(5)
    responses["D2"] = [1, 1, 1]              # make D2 the weakest
    responses["D6"] = [2, 2, 2]              # D6 second weakest
    result = commercial_health_index(responses, FW)
    gap_ids = [g["id"] for g in result["gaps"]]
    assert gap_ids[0] == "D2"
    assert "D6" in gap_ids


def test_chi_no_input_is_none():
    result = commercial_health_index({}, FW)
    assert result["chi"] is None
    assert result["band"] is None
