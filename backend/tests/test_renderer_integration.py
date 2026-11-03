from app.scenario_generator.renderer import (
    render_generated_scenarios
)


def test_render_generated_scenarios():
    generated_result = {
        "rule_id": "TEST001",
        "scenarios": [
            {
                "scenario_id": "TEST001-S001",
                "rule_id": "TEST001",
                "patient_profile": {
                    "age": 45,
                    "kidney_function": 90
                }
            },
            {
                "scenario_id": "TEST001-S002",
                "rule_id": "TEST001",
                "patient_profile": {
                    "age": 45,
                    "kidney_function": 60
                }
            }
        ]
    }

    template = (
        "A patient aged {age} has a recorded "
        "kidney_function value of {kidney_function}."
    )

    result = render_generated_scenarios(
        generated_result,
        template
    )

    assert result["total_rendered"] == 2

    assert result["rendered_scenarios"][0]["prompt"] == (
        "A patient aged 45 has a recorded "
        "kidney_function value of 90."
    )

    assert result["rendered_scenarios"][1]["prompt"] == (
        "A patient aged 45 has a recorded "
        "kidney_function value of 60."
    )

    assert "expected_safe_behavior" not in str(result)