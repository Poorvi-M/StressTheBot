
from app.schemas.rule_schema import ClinicalRule
from app.scenario_generator.generator import generate_scenarios


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


def test_generate_valid_scenarios():
    rule = create_test_rule()

    parameter_sets = [
        {"age": 45, "kidney_function": 90},
        {"age": 45, "kidney_function": 60}
    ]

    result = generate_scenarios(
        rule,
        parameter_sets
    )

    assert result["total_generated"] == 2
    assert result["total_rejected"] == 0

    assert result["scenarios"][0]["rule_id"] == "TEST001"


def test_reject_missing_parameters():
    rule = create_test_rule()

    parameter_sets = [
        {"age": 45}
    ]

    result = generate_scenarios(
        rule,
        parameter_sets
    )

    assert result["total_generated"] == 0
    assert result["total_rejected"] == 1


def test_reject_invalid_parameter_values():
    rule = create_test_rule()

    parameter_sets = [
        {"age": 15, "kidney_function": 60}
    ]

    constraints = {
        "age": {"min": 18, "max": 100}
    }

    result = generate_scenarios(
        rule,
        parameter_sets,
        constraints
    )

    assert result["total_generated"] == 0
    assert result["total_rejected"] == 1
