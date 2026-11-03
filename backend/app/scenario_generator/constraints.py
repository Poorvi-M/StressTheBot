
from typing import Any


def validate_parameters(
    parameters: dict[str, Any],
    required_parameters: list[str],
    parameter_constraints: dict[str, dict] | None = None
) -> tuple[bool, list[str]]:

    errors = []
    parameter_constraints = parameter_constraints or {}

    # 1. Check whether required parameters are present
    for parameter in required_parameters:
        if parameter not in parameters:
            errors.append(
                f"Missing required parameter: {parameter}"
            )

    # 2. Validate individual parameter constraints
    for parameter, value in parameters.items():

        constraints = parameter_constraints.get(parameter, {})

        # 3. Validate data type
        data_type = constraints.get("data_type")

        if data_type == "integer":
            if not isinstance(value, int) or isinstance(value, bool):
                errors.append(
                    f"{parameter} must be an integer"
                )
                continue

        elif data_type == "number":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(
                    f"{parameter} must be numeric"
                )
                continue

        elif data_type == "string":
            if not isinstance(value, str):
                errors.append(
                    f"{parameter} must be a string"
                )
                continue

        elif data_type == "boolean":
            if not isinstance(value, bool):
                errors.append(
                    f"{parameter} must be a boolean"
                )
                continue

        elif data_type == "categorical":
            if not isinstance(value, str):
                errors.append(
                    f"{parameter} must be a string category"
                )
                continue

        # 4. Check allowed values
        allowed_values = constraints.get("allowed_values")

        if allowed_values is not None:
            if value not in allowed_values:
                errors.append(
                    f"{parameter} must be one of {allowed_values}"
                )

        # 5. Check minimum value
        minimum = constraints.get("minimum")

        if minimum is None:
            minimum = constraints.get("min")

        if minimum is not None:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(
                    f"{parameter} must be numeric"
                )
            elif value < minimum:
                errors.append(
                    f"{parameter} must be at least {minimum}"
                )

        # 6. Check maximum value
        maximum = constraints.get("maximum")

        if maximum is None:
            maximum = constraints.get("max")

        if maximum is not None:
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                errors.append(
                    f"{parameter} must be numeric"
                )
            elif value > maximum:
                errors.append(
                    f"{parameter} must not exceed {maximum}"
                )

    return len(errors) == 0, errors
