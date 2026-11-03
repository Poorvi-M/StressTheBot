
from typing import Any


def generate_parameter_sweep(
    base_profile: dict[str, Any],
    parameter: str,
    values: list[Any]
) -> list[dict[str, Any]]:

    if not isinstance(base_profile, dict):
        raise TypeError("base_profile must be a dictionary")

    if not parameter or not isinstance(parameter, str):
        raise ValueError("Parameter name must be a non-empty string")

    if parameter not in base_profile:
        raise ValueError(
            f"Parameter '{parameter}' is not present in the base profile"
        )

    if not isinstance(values, list) or not values:
        raise ValueError("Sweep values must be a non-empty list")

    # Reject duplicate values to avoid duplicate scenarios.
    for index, value in enumerate(values):
        if value in values[:index]:
            raise ValueError(
                f"Duplicate sweep value found: {value}"
            )

    scenarios = []

    for value in values:
        # Copy the profile so the original remains unchanged.
        profile = base_profile.copy()

        profile[parameter] = value

        scenarios.append(profile)

    return scenarios
