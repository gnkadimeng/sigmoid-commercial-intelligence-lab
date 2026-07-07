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


# ---------------------------------------------------------------------------
# Evidence Operating Layer (Phase 1) — register schemas + value validators
# ---------------------------------------------------------------------------

# Required columns for each register (used by validate_* helpers and the data-integrity tests).
DECISION_REGISTER_COLUMNS = [
    "decision_id", "decision_name", "decision_question", "current_status",
    "current_hypothesis", "current_confidence_grade", "required_confidence_grade",
    "linked_frameworks", "linked_dashboards", "next_experiment", "owner", "last_reviewed",
]

CLAIM_REGISTER_COLUMNS = [
    "claim_id", "decision_id", "claim_text", "claim_type", "current_confidence_grade",
    "status", "evidence_needed_for_B", "evidence_needed_for_A", "owner", "last_reviewed",
]

DISCOVERY_INTERVIEW_COLUMNS = [
    "interview_id", "date", "company_segment", "company_size", "respondent_role",
    "decision_linked", "claim_linked", "pain_score", "budget_signal", "urgency_signal",
    "current_tooling", "crm_maturity", "workflow_maturity", "ai_readiness_maturity",
    "positioning_preference", "willingness_to_pay_signal", "sales_cycle_signal", "notes",
    "evidence_quality_score", "bias_risk", "supports_or_refutes",
]

DISCOVERY_EVIDENCE_COLUMNS = [
    "evidence_id", "interview_id", "decision_id", "claim_id", "source_type", "source_name",
    "date_collected", "quality_score", "bias_risk", "supports_or_refutes",
    "evidence_summary", "confidence_impact", "notes",
]

# The 0–100 signal columns in a discovery interview (quality_score is 0–1, handled separately).
INTERVIEW_SCORE_COLUMNS = [
    "pain_score", "budget_signal", "urgency_signal", "crm_maturity", "workflow_maturity",
    "ai_readiness_maturity", "willingness_to_pay_signal", "sales_cycle_signal",
]

VALID_CONFIDENCE_GRADES = {"A", "B", "C", "D"}
VALID_SUPPORTS_VALUES = {"supports", "refutes", "mixed", "neutral"}


def validate_decision_register(df) -> bool:
    """Assert the decision register has its required columns."""
    return validate_required_columns(df, DECISION_REGISTER_COLUMNS)


def validate_claim_register(df) -> bool:
    """Assert the claim register has its required columns."""
    return validate_required_columns(df, CLAIM_REGISTER_COLUMNS)


def validate_discovery_interviews(df) -> bool:
    """Assert the discovery-interview dataset has its required columns."""
    return validate_required_columns(df, DISCOVERY_INTERVIEW_COLUMNS)


def validate_discovery_evidence(df) -> bool:
    """Assert the processed discovery-evidence dataset has its required columns."""
    return validate_required_columns(df, DISCOVERY_EVIDENCE_COLUMNS)


def validate_confidence_grades(df, columns: Iterable[str]) -> bool:
    """Assert that every value in the given grade columns is one of A, B, C, D.

    Missing values are ignored (a grade may legitimately be blank). Raises ``ValueError`` naming the
    offending column and values otherwise. Absent columns are reported as an error.
    """
    problems: list[str] = []
    for col in columns:
        if col not in df.columns:
            problems.append(f"missing column: {col}")
            continue
        values = df[col].dropna().astype(str).str.strip().str.upper()
        invalid = sorted(set(values) - VALID_CONFIDENCE_GRADES)
        if invalid:
            problems.append(f"invalid grades in '{col}': {invalid}")
    if problems:
        raise ValueError("; ".join(problems))
    return True


def validate_supports_or_refutes(df, column: str = "supports_or_refutes") -> bool:
    """Assert that a support column contains only supports / refutes / mixed / neutral.

    Missing values are ignored. Raises ``ValueError`` naming the offending values otherwise.
    """
    if column not in df.columns:
        raise ValueError(f"missing column: {column}")
    values = df[column].dropna().astype(str).str.strip().str.lower()
    invalid = sorted(set(values) - VALID_SUPPORTS_VALUES)
    if invalid:
        raise ValueError(f"invalid {column} values: {invalid}")
    return True


def validate_scores_in_range(df, columns: Iterable[str], low: float = 0.0,
                             high: float = 100.0) -> bool:
    """Assert that numeric values in the given columns fall within [low, high].

    Missing / unparseable values are ignored; genuine out-of-range numbers raise ``ValueError``.
    Absent columns are reported as an error rather than silently skipped.
    """
    problems: list[str] = []
    for col in columns:
        if col not in df.columns:
            problems.append(f"missing column: {col}")
            continue
        numeric = df[col].map(to_float).dropna()
        out = numeric[(numeric < low) | (numeric > high)]
        if len(out):
            problems.append(f"'{col}' has values outside [{low}, {high}]: {sorted(out.unique())}")
    if problems:
        raise ValueError("; ".join(problems))
    return True
