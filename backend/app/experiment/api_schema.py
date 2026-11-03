from typing import Any
from pydantic import BaseModel, Field

from app.evaluation.evaluation_schema import EvaluationCheck


class ExperimentRequest(BaseModel):
    rule_id: str
    parameter_sets: list[dict[str, Any]] = Field(min_length=1)
    template: str = Field(min_length=1)
    checks: list[EvaluationCheck] = Field(min_length=1)
    providers: list[str] | None = None
    parameter_constraints: dict[str, dict] | None = None