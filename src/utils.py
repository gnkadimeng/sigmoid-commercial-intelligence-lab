"""Shared helpers: filesystem paths, safe numerics, and loaders for data + frameworks.

Kept deliberately small and dependency-light. `pandas` and `pyyaml` are the only hard deps here; the
numeric helpers work on plain dicts and pandas rows alike so scoring functions can be tested without
loading any files.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Mapping

# --- Project paths -----------------------------------------------------------------

# src/ lives one level below the project root.
PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
DATA_DIR: Path = PROJECT_ROOT / "data"
SAMPLE_DIR: Path = DATA_DIR / "sample"
FRAMEWORKS_DIR: Path = PROJECT_ROOT / "frameworks"


# --- Safe numerics -----------------------------------------------------------------

def to_float(value: Any) -> float | None:
    """Coerce a value to float, returning None for missing/blank/non-numeric/NaN.

    Handles the awkward cases that crash naive scoring code: None, empty strings,
    pandas NaN, and stray text.
    """
    if value is None:
        return None
    if isinstance(value, str) and value.strip() == "":
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(result):
        return None
    return result


def get_num(row: Mapping[str, Any], key: str) -> float | None:
    """Fetch ``row[key]`` as a float, tolerating missing keys and bad values.

    Works for dicts and pandas Series alike.
    """
    try:
        value = row[key]
    except (KeyError, IndexError, TypeError):
        return None
    return to_float(value)


def get_str(row: Mapping[str, Any], key: str, default: str = "") -> str:
    """Fetch ``row[key]`` as a lowercased, stripped string, tolerating missing keys."""
    try:
        value = row[key]
    except (KeyError, IndexError, TypeError):
        return default
    if value is None:
        return default
    text = str(value).strip().lower()
    return text if text else default


def clamp(value: float, low: float, high: float) -> float:
    """Constrain ``value`` to the inclusive range [low, high]."""
    return max(low, min(high, value))


# --- Loaders -----------------------------------------------------------------------

def load_sample(name: str):
    """Load a CSV from data/sample/ into a DataFrame (import pandas lazily)."""
    import pandas as pd

    path = SAMPLE_DIR / name
    return pd.read_csv(path)


def load_framework(name: str) -> dict:
    """Load a framework YAML from frameworks/ (with or without the .yml suffix)."""
    import yaml

    filename = name if name.endswith((".yml", ".yaml")) else f"{name}.yml"
    path = FRAMEWORKS_DIR / filename
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def weights_from_framework(framework: dict) -> dict[str, dict]:
    """Convert a framework's ``criteria`` list into a scoring weight dict.

    Returns ``{criterion_name: {"weight": float, "direction": str}}`` — the shape the
    scoring functions consume. Lets a dashboard drive scoring straight from the YAML.
    """
    weights: dict[str, dict] = {}
    for criterion in framework.get("criteria", []):
        weights[criterion["name"]] = {
            "weight": float(criterion.get("weight", 0.0)),
            "direction": criterion.get("direction", "higher_better"),
        }
    return weights
