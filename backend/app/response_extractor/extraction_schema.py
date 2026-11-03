
from typing import Literal

from pydantic import BaseModel, Field


class SafetyObservation(BaseModel):
    """
    A structured observation extracted from an LLM response.

    This records what the model explicitly stated.
    It does not determine whether the statement is clinically correct.
    """

    category: Literal[
        "medication_safety",
        "kidney_risk",
        "herbal_remedy_safety",
        "supplement_safety",
        "monitoring",
        "contraindication",
        "uncertainty",
        "other"
    ]

    statement: str

    evidence_text: str

    explicitly_stated: bool = True


class ExtractedResponse(BaseModel):

    scenario_id: str
    provider: str
    model: str

    medication_recommendations: list[str] = Field(
        default_factory=list
    )

    contraindication_warnings: list[str] = Field(
        default_factory=list
    )

    safety_alerts: list[str] = Field(
        default_factory=list
    )

    monitoring_recommendations: list[str] = Field(
        default_factory=list
    )

    alternative_suggestions: list[str] = Field(
        default_factory=list
    )

    rationale: list[str] = Field(
        default_factory=list
    )

    uncertainty_statements: list[str] = Field(
        default_factory=list
    )

    safety_observations: list[SafetyObservation] = Field(
        default_factory=list
    )

    raw_response: str
