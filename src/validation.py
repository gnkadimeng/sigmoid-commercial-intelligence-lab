"""Structural data-integrity validation (CIS §12, layer 1).

These checks guard the *shape* of data before it is scored or published. They are intentionally
plain: predicates that answer yes/no, and assertions that raise ``ValueError`` with a clear message
when an integrity rule is broken. Decision-level validation (confidence vs evidence strength) lives
with the evidence/recommendation logic, not here.

``pandera``/``pydantic`` schema enforcement is noted as Future Work; at v0.1 these functions cover
the required guarantees with no heavy dependency.
"""

from __future__ import annotations

from typing import Iterable

from .utils import to_float


def validate_score_range(value, low: float = 0.0, high: float = 100.0) -> bool:
    """Return True iff ``value`` is numeric and within the inclusive range [low, high].

    A predicate — safe to call on anything. Non-numeric or missing values return False.
    """
    number = to_float(value)
    if number is None:
        return False
    return low <= number <= high


def validate_required_columns(df, required_columns: Iterable[str]) -> bool:
    """Assert that ``df`` contains every column in ``required_columns``.

    Returns True when all are present; raises ``ValueError`` naming the missing columns otherwise.
    """
    present = set(df.columns)
    missing = [col for col in required_columns if col not in present]
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return True


def validate_no_negative_scores(df, score_columns: Iterable[str]) -> bool:
    """Assert that none of the given score columns contain negative values.

    Returns True when clean; raises ``ValueError`` naming the offending columns otherwise. Columns
    absent from ``df`` are reported as an error rather than silently skipped.
    """
    offenders: list[str] = []
    missing: list[str] = []
    for col in score_columns:
        if col not in df.columns:
            missing.append(col)
            continue
        numeric = df[col].map(to_float)
        # Ignore None (missing) but flag any genuine negative number.
        if numeric.dropna().lt(0).any():
            offenders.append(col)

    problems = []
    if missing:
        problems.append(f"missing columns: {sorted(missing)}")
    if offenders:
        problems.append(f"negative values in: {sorted(offenders)}")
    if problems:
        raise ValueError("; ".join(problems))
    return True
