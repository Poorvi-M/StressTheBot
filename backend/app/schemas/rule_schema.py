
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl, model_validator


class ParameterDefinition(BaseModel):
    name: str
    data_type: Literal[
        "integer", "number", "string", "boolean", "categorical"
    ]
    description: str = ""
    unit: str | None = None
    required: bool = True
    minimum: int | float | None = None
    maximum: int | float | None = None
    allowed_values: list[Any] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_definition(self):
        if (
            self.minimum is not None
            and self.maximum is not None
            and self.minimum > self.maximum
        ):
            raise ValueError("minimum cannot be greater than maximum")

        if self.data_type == "categorical" and not self.allowed_values:
            raise ValueError(
                "Categorical parameters must define allowed_values"
            )

        if self.data_type in ("integer", "number"):
            if self.allowed_values:
                raise ValueError(
                    "Numeric parameters should use minimum and maximum, "
                    "not allowed_values"
                )
        else:
            if self.minimum is not None or self.maximum is not None:
                raise ValueError(
                    "minimum and maximum are only valid for numeric parameters"
                )

        return self


class ClinicalRule(BaseModel):
    rule_id: str
    title: str
    category: str

    # Source provenance
    source_name: str
    source_url: HttpUrl
    source_excerpt: str
    source_publication_date: str | None = None
    source_version: str | None = None
    source_section: str | None = None
    source_page: str | None = None

    # Clinical rule definition
    applicability_conditions: list[str] = Field(min_length=1)
    expected_safe_behavior: list[str] = Field(min_length=1)
    parameters: list[str] = Field(default_factory=list)
    parameter_definitions: list[ParameterDefinition] = Field(
        default_factory=list
    )

    # Risk assessment
    severity: Literal["low", "medium", "high", "critical"]
    severity_rationale: str | None = None

    # Review and approval
    status: Literal["draft", "approved"] = "draft"
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    review_notes: str | None = None

    @model_validator(mode="after")
    def validate_rule(self):
        parameter_names = self.parameters
        definition_names = [
            definition.name for definition in self.parameter_definitions
        ]

        if len(parameter_names) != len(set(parameter_names)):
            raise ValueError("Duplicate parameter names are not allowed")

        if len(definition_names) != len(set(definition_names)):
            raise ValueError(
                "Duplicate parameter definitions are not allowed"
            )

        if set(parameter_names) != set(definition_names):
            raise ValueError(
                "parameters and parameter_definitions must contain "
                "the same parameter names"
            )

        if self.status == "approved":
            if not self.reviewed_by or not self.reviewed_at:
                raise ValueError(
                    "Approved rules must include reviewer and review date"
                )

        return self
