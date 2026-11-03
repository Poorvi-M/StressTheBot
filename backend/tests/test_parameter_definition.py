import pytest
from pydantic import ValidationError

from app.schemas.rule_schema import ParameterDefinition, ClinicalRule


def test_valid_numeric_parameter():

    parameter = ParameterDefinition(
        name="sample_value",
        data_type="number",
        description="Software test parameter",
        minimum=0,
        maximum=100
    )

    assert parameter.name == "sample_value"
    assert parameter.data_type == "number"
    assert parameter.minimum == 0
    assert parameter.maximum == 100


def test_valid_categorical_parameter():

    parameter = ParameterDefinition(
        name="sample_category",
        data_type="categorical",
        allowed_values=["A", "B", "C"]
    )

    assert parameter.allowed_values == ["A", "B", "C"]


def test_categorical_parameter_requires_allowed_values():

    with pytest.raises(ValidationError):
        ParameterDefinition(
            name="sample_category",
            data_type="categorical"
        )


def test_minimum_cannot_exceed_maximum():

    with pytest.raises(ValidationError):
        ParameterDefinition(
            name="sample_value",
            data_type="number",
            minimum=100,
            maximum=10
        )


def test_string_parameter_rejects_numeric_bounds():

    with pytest.raises(ValidationError):
        ParameterDefinition(
            name="sample_text",
            data_type="string",
            minimum=1
        )


def test_clinical_rule_accepts_parameter_definitions():

    rule = ClinicalRule(
        rule_id="TEST002",
        title="Schema testing rule",
        category="test",
        source_name="Software Testing Placeholder",
        source_url="https://example.com/test",
        source_excerpt="Placeholder content.",
        applicability_conditions=["Software testing only"],
        expected_safe_behavior=["Validate the parameter"],
        parameters=["sample_value"],
        parameter_definitions=[
            ParameterDefinition(
                name="sample_value",
                data_type="integer",
                minimum=1,
                maximum=10
            )
        ],
        severity="low",
        status="draft"
    )

    assert len(rule.parameter_definitions) == 1
    assert rule.parameter_definitions[0].name == "sample_value"