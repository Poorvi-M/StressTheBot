
from typing import Any

from app.schemas.rule_schema import ClinicalRule
from app.scenario_generator.constraints import validate_parameters
from app.scenario_generator.parameter_sweep import generate_parameter_sweep


def _build_parameter_constraints(
    rule: ClinicalRule,
    additional_constraints: dict[str, dict] | None = None
) -> tuple[list[str], dict[str, dict]]:

    required_parameters = []
    parameter_constraints = {}

    additional_constraints = additional_constraints or {}

    if not isinstance(additional_constraints, dict):
        raise TypeError("Additional constraints must be a dictionary")

    unknown_constraints = (
        set(additional_constraints.keys()) - set(rule.parameters)
    )

    if unknown_constraints:
        raise ValueError(
            f"Constraints provided for undefined parameters: "
            f"{sorted(unknown_constraints)}"
        )

    for definition in rule.parameter_definitions:

        if definition.required:
            required_parameters.append(definition.name)

        constraints = {
            "data_type": definition.data_type,
            "allowed_values": definition.allowed_values or None,
            "minimum": definition.minimum,
            "maximum": definition.maximum
        }

        extra = additional_constraints.get(definition.name, {})

        if not isinstance(extra, dict):
            raise TypeError(
                f"Constraints for '{definition.name}' must be a dictionary"
            )

        # Accept both naming conventions for numeric limits.
        extra_min = extra.get("minimum", extra.get("min"))
        extra_max = extra.get("maximum", extra.get("max"))

        # Additional constraints can tighten, never loosen,
        # the limits defined by the clinical rule.
        if extra_min is not None:
            existing_min = constraints["minimum"]
            constraints["minimum"] = (
                max(existing_min, extra_min)
                if existing_min is not None
                else extra_min
            )

        if extra_max is not None:
            existing_max = constraints["maximum"]
            constraints["maximum"] = (
                min(existing_max, extra_max)
                if existing_max is not None
                else extra_max
            )

        # Intersect additional categorical values with
        # the values permitted by the clinical rule.
        if extra.get("allowed_values") is not None:

            extra_values = extra["allowed_values"]

            if not isinstance(extra_values, list):
                raise TypeError(
                    f"allowed_values for '{definition.name}' "
                    "must be a list"
                )

            defined_values = constraints["allowed_values"]

            if defined_values is not None:
                constraints["allowed_values"] = [
                    value for value in defined_values
                    if value in extra_values
                ]
            else:
                constraints["allowed_values"] = extra_values

        minimum = constraints["minimum"]
        maximum = constraints["maximum"]

        if (
            minimum is not None
            and maximum is not None
            and minimum > maximum
        ):
            raise ValueError(
                f"Contradictory constraints for '{definition.name}': "
                f"minimum ({minimum}) exceeds maximum ({maximum})"
            )

        parameter_constraints[definition.name] = constraints

    return required_parameters, parameter_constraints


def generate_scenarios(
    rule: ClinicalRule,
    parameter_sets: list[dict[str, Any]],
    parameter_constraints: dict[str, dict] | None = None
) -> dict:

    scenarios = []
    rejected_scenarios = []

    required_parameters, derived_constraints = (
        _build_parameter_constraints(
            rule,
            parameter_constraints
        )
    )

    for index, parameters in enumerate(parameter_sets, start=1):

        errors = []

        if not isinstance(parameters, dict):
            rejected_scenarios.append({
                "scenario_number": index,
                "rule_id": rule.rule_id,
                "parameters": parameters,
                "errors": ["Scenario parameters must be a dictionary"]
            })
            continue

        # Reject parameters not defined by the clinical rule.
        unknown_parameters = (
            set(parameters.keys()) - set(rule.parameters)
        )

        for parameter in sorted(unknown_parameters):
            errors.append(
                f"Unknown parameter: {parameter}"
            )

        _, validation_errors = validate_parameters(
            parameters=parameters,
            required_parameters=required_parameters,
            parameter_constraints=derived_constraints
        )

        errors.extend(validation_errors)

        if errors:
            rejected_scenarios.append({
                "scenario_number": index,
                "rule_id": rule.rule_id,
                "parameters": parameters,
                "errors": errors
            })

            continue

        scenario = {
            "scenario_id": f"{rule.rule_id}-S{index:03d}",
            "rule_id": rule.rule_id,
            "patient_profile": parameters.copy()
        }

        scenarios.append(scenario)

    return {
        "rule_id": rule.rule_id,
        "total_generated": len(scenarios),
        "total_rejected": len(rejected_scenarios),
        "scenarios": scenarios,
        "rejected_scenarios": rejected_scenarios
    }


def generate_scenarios_from_sweep(
    rule: ClinicalRule,
    base_profile: dict[str, Any],
    parameter: str,
    values: list[Any],
    parameter_constraints: dict[str, dict] | None = None
) -> dict:

    if parameter not in rule.parameters:
        raise ValueError(
            f"'{parameter}' is not an applicable parameter "
            f"for rule '{rule.rule_id}'"
        )

    parameter_sets = generate_parameter_sweep(
        base_profile=base_profile,
        parameter=parameter,
        values=values
    )

    result = generate_scenarios(
        rule=rule,
        parameter_sets=parameter_sets,
        parameter_constraints=parameter_constraints
    )

    result["sweep"] = {
        "parameter": parameter,
        "values": values,
        "base_profile": base_profile
    }

    return result
