
from typing import Literal, Any

from pydantic import BaseModel, Field


class RiskRecord(BaseModel):
    scenario_id: str
    provider: str
    model: str
    rule_id: str

    status: Literal[
        "potential_violation",
        "missing_expected_behavior",
        "no_detected_issue",
        "manual_review"
    ]

    severity: Literal["low", "medium", "high", "critical"]

    patient_parameters: dict[str, Any] = Field(
        default_factory=dict
    )

    matched_prohibited_patterns: list[str] = Field(
        default_factory=list
    )

    missing_required_patterns: list[str] = Field(
        default_factory=list
    )

    # Extracted evidence supporting the evaluation.
    evidence: list[dict[str, str]] = Field(
        default_factory=list
    )

    explanation: str

    requires_human_review: bool = True
