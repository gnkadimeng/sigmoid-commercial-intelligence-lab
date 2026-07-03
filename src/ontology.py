"""Lightweight Python types mirroring the CIS core ontology (v0.1).

These are intentionally simple ``dataclass`` records — enough to represent, pass around, and validate
the shape of the decision objects, without imposing a database or ORM at v0.1. The normative
definitions live in ``cis/ontology.yml`` and ``cis/object-model.yml``; these classes are the
convenient in-code counterpart.

Confidence grades (D..A) and lifecycle stages are provided as constants so code can refer to them by
name rather than magic strings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

# Confidence grades, worst to best (see CIS §17).
CONFIDENCE_GRADES = ("D", "C", "B", "A")
CONFIDENCE_MEANING = {
    "D": "Hypothesis — asserted, not yet evidenced.",
    "C": "Indicative — weak/illustrative evidence.",
    "B": "Substantiated — moderate, corroborated evidence.",
    "A": "Validated — strong evidence, method validated, monitored.",
}

# Ordered decision lifecycle stages (see cis/decision-lifecycle.yml).
LIFECYCLE_STAGES = (
    "question",
    "hypothesis",
    "operational_definition",
    "evidence_collection",
    "analysis",
    "model",
    "validation",
    "recommendation",
    "implementation",
    "monitoring",
    "learning",
)


@dataclass
class Question:
    id: str
    text: str
    domain: str = "other"           # market | positioning | pricing | ai_readiness | gtm | other
    priority: str = "medium"        # low | medium | high
    status: str = "active"


@dataclass
class Hypothesis:
    id: str
    question_id: str
    statement: str
    falsifier: str                  # what observation would refute this
    status: str = "draft"


@dataclass
class Evidence:
    id: str
    claim_id: str
    source_type: str                # proposal | interview | survey | market_report | ...
    source_name: str
    quality_score: float            # 0..1
    bias_risk: str                  # low | medium | high
    supports_claim: str             # yes | no | mixed
    date_collected: Optional[str] = None
    notes: str = ""


@dataclass
class Framework:
    id: str
    version: str
    question: str
    criteria: List[dict] = field(default_factory=list)  # each: name, weight, direction
    scale: str = "0..100"
    status: str = "draft"


@dataclass
class Model:
    id: str
    version: str
    kind: str                       # framework | statistical | ml | rule_set
    output: str
    inputs: List[str] = field(default_factory=list)
    framework_id: Optional[str] = None


@dataclass
class Recommendation:
    id: str
    question_id: str
    action: str
    confidence: str                 # A | B | C | D
    basis: str
    models: List[str] = field(default_factory=list)      # model ids cited
    evidence: List[str] = field(default_factory=list)    # evidence ids cited

    def is_valid(self) -> bool:
        """A recommendation is valid only if it cites at least one model and one evidence item,
        and carries a recognised confidence grade (CIS §12, decision-level validation)."""
        return (
            bool(self.models)
            and bool(self.evidence)
            and self.confidence in CONFIDENCE_GRADES
        )


@dataclass
class Decision:
    id: str
    question_id: str
    recommendation_id: str
    owner: str
    confidence: str = "C"
    basis: str = ""
    date: Optional[str] = None
    status: str = "proposed"        # proposed | adopted | superseded | reversed
