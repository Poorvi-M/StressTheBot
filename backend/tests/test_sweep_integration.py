
import pytest

from app.schemas.rule_schema import ClinicalRule

from app.scenario_generator.generator import (
    generate_scenarios_from_sweep
)


def create_test_rule():
    return ClinicalRule(
        rule_id="TEST001",
        title="Sample testing rule",
        category="medication_safety",
        source_name="Software Testing Placeholder",
        source_url="https://example.com/test-rule",
        source_excerpt="Placeholder testing content.",

        applicability_conditions=[
            "Testing condition"
        ],
        expected_safe_behavior=[
            "Testing behaviour"
        ],

        parameters=["age", "kidney_function"],

        parameter_definitions=[
            {
                "name": "age",
                "data_type": "integer",
                "description": "Synthetic age used for software testing",
                "unit": "years",
                "required": True,
                "minimum": 18,
                "maximum": 100,
                "allowed_values": []
            },
            {
                "name": "kidney_function",
                "data_type": "number",
                "description": "Placeholder kidney function value used for software testing",
                "unit": "test_units",
                "required": True,
                "minimum": 0,
                "maximum": 120,
                "allowed_values": []
            }
        ],

        severity="low",
        severity_rationale="Placeholder severity for software testing.",
        status="draft",
        reviewed_by=None,
        reviewed_at=None,
        review_notes=None
    )


def test_sweep_generates_valid_scenarios():
    rule = create_test_rule()

    base_profile = {
        "age": 45,
        "kidney_function": 90
    }

    values = [90, 75, 60, 45, 30]

    constraints = {
        "age": {"min": 18, "max": 100},
        "kidney_function": {"min": 0, "max": 120}
    }

    result = generate_scenarios_from_sweep(
        rule,
        base_profile,
        "kidney_function",
        values,
        constraints
    )

    assert result["total_generated"] == 5
    assert result["total_rejected"] == 0


def test_sweep_rejects_invalid_profiles():
    rule = create_test_rule()

    base_profile = {
        "age": 45,
        "kidney_function": 90
    }

    result = generate_scenarios_from_sweep(
        rule,
        base_profile,
        "age",
        [45, 15, 60],
        {"age": {"min": 18, "max": 100}}
    )

    assert result["total_generated"] == 2
    assert result["total_rejected"] == 1


def test_sweep_rejects_inapplicable_parameter():
    rule = create_test_rule()

    base_profile = {
        "age": 45,
        "kidney_function": 90
    }

    with pytest.raises(ValueError):
        generate_scenarios_from_sweep(
            rule,
            base_profile,
            "weight",
            [50, 60, 70]
        )
