from typing import Literal
from pydantic import BaseModel, Field


EvaluationStatus = Literal[
    "potential_violation",
    "missing_expected_behavior",
    "no_detected_issue",
    "manual_review"
]


class EvaluationCheck(BaseModel):
    rule_id: str

    # Text patterns that indicate a potentially unsafe response.
    prohibited_patterns: list[str] = Field(default_factory=list)

    # At least one of these patterns must appear when the
    # rule applies. Otherwise, expected behavior may be missing.
    required_patterns: list[str] = Field(default_factory=list)

    # Whether this check applies to the supplied scenario.
    applicable: bool = True

    severity: Literal["low", "medium", "high", "critical"]


class RuleEvaluationResult(BaseModel):
    scenario_id: str
    provider: str
    model: str
    rule_id: str
    status: EvaluationStatus
    severity: str
    matched_prohibited_patterns: list[str] = Field(
        default_factory=list
    )
    missing_required_patterns: list[str] = Field(
        default_factory=list
    )
    explanation: str
    requires_human_review: bool = False