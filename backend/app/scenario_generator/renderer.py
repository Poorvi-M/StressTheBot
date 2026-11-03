from string import Formatter
from typing import Any


def render_scenario(
    patient_profile: dict[str, Any],
    template: str
) -> str:
    """
    Convert a structured patient profile into a natural-language scenario.

    The template must be reviewed and supplied by the project team.
    Only values from patient_profile can be inserted.
    """

    if not template or not template.strip():
        raise ValueError("Scenario template cannot be empty")

    if not patient_profile:
        raise ValueError("Patient profile cannot be empty")

    formatter = Formatter()

    # Check that every placeholder refers to a field in the profile.
    for _, field_name, format_spec, conversion in formatter.parse(template):
        if field_name is None:
            continue

        if not field_name.isidentifier():
            raise ValueError(
                f"Invalid template placeholder: {field_name}"
            )

        if field_name not in patient_profile:
            raise ValueError(
                f"Template field '{field_name}' is missing "
                "from the patient profile"
            )

        if format_spec or conversion:
            raise ValueError(
                "Format specifications and conversions are not allowed"
            )

    # Insert only patient profile values.
    return template.format_map(patient_profile)
def render_generated_scenarios(
    generated_result: dict,
    template: str
) -> dict:
    """
    Render every generated scenario using the supplied template.
    """

    rendered_scenarios = []

    for scenario in generated_result["scenarios"]:
        prompt = render_scenario(
            patient_profile=scenario["patient_profile"],
            template=template
        )

        rendered_scenarios.append({
            "scenario_id": scenario["scenario_id"],
            "prompt": prompt
        })

    return {
        "rule_id": generated_result["rule_id"],
        "total_rendered": len(rendered_scenarios),
        "rendered_scenarios": rendered_scenarios
    }