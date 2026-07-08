"""Tests for the Message House canonical data (frameworks/message_house.yml).

The interactive navigator is only trustworthy if the data behind it is well-formed:
five pillars, every toolkit item tagged to a real pillar, and every pillar used.
"""

import pathlib

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
MH = yaml.safe_load((ROOT / "frameworks" / "message_house.yml").read_text())

PILLAR_IDS = [p["id"] for p in MH["pillars"]]


def test_apex_is_commercial_health_with_a_link():
    assert MH["apex"]["name"] == "Commercial Health"
    assert MH["apex"]["link"] and MH["apex"]["link_text"]
    assert MH["apex"]["meaning"].strip()


def test_five_pillars_with_required_fields():
    assert len(MH["pillars"]) == 5
    for p in MH["pillars"]:
        assert p["id"] and p["name"] and p["sub"] and p["question"]
    assert PILLAR_IDS == ["find", "win", "keep", "grow", "decide"]


def test_toolkit_categories_have_labels_and_items():
    assert MH["toolkit"]
    for cat in MH["toolkit"]:
        assert cat["key"] and cat["label"]
        assert cat["items"], f"{cat['key']} has no items"


def test_every_item_tags_only_known_pillars():
    for cat in MH["toolkit"]:
        for it in cat["items"]:
            assert it.get("text"), f"empty text in {cat['key']}"
            tags = it.get("pillars", [])
            assert tags, f"item has no pillar tag: {it['text']!r}"
            for t in tags:
                assert t in PILLAR_IDS, f"unknown pillar {t!r} in {cat['key']}"


def test_every_pillar_has_at_least_one_item():
    tagged = {t for cat in MH["toolkit"] for it in cat["items"] for t in it.get("pillars", [])}
    for pid in PILLAR_IDS:
        assert pid in tagged, f"pillar {pid} has no toolkit material"


@pytest.mark.parametrize("cat_key", ["beliefs", "problems", "questions", "myths", "jtbd", "outcomes", "signature_ideas"])
def test_expected_reservoirs_present(cat_key):
    keys = [c["key"] for c in MH["toolkit"]]
    assert cat_key in keys
