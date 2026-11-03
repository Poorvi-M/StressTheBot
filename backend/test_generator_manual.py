
from app.schemas.rule_schema import ClinicalRule

from app.scenario_generator.generator import (
    generate_scenarios_from_sweep
)


rule = ClinicalRule(
    rule_id="TEST001",
    title="Sample testing rule",
    category="medication_safety",
    source_name="Software Testing Placeholder",
    source_url="https://example.com/test-rule",
    source_excerpt="Placeholder content.",

    applicability_conditions=["Testing condition"],
    expected_safe_behavior=["Testing behaviour"],

    parameters=["age", "kidney_function"],

    parameter_definitions=[
        {
            "name": "age",
            "data_type": "integer",
            "description": "Age used for software testing",
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
    status="draft"
)


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
    rule=rule,
    base_profile=base_profile,
    parameter="kidney_function",
    values=values,
    parameter_constraints=constraints
)


print(result)
