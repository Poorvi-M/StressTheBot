import pytest

from app.scenario_generator.parameter_sweep import (
    generate_parameter_sweep
)


def test_generate_parameter_sweep():

    base_profile = {
        "age": 45,
        "kidney_function": 90
    }

    values = [90, 75, 60, 45, 30]

    result = generate_parameter_sweep(
        base_profile,
        "kidney_function",
        values
    )

    assert len(result) == 5

    assert result[0]["kidney_function"] == 90
    assert result[1]["kidney_function"] == 75
    assert result[4]["kidney_function"] == 30

    assert all(
        profile["age"] == 45
        for profile in result
    )


def test_original_profile_remains_unchanged():

    base_profile = {
        "age": 45,
        "kidney_function": 90
    }

    generate_parameter_sweep(
        base_profile,
        "kidney_function",
        [90, 60, 30]
    )

    assert base_profile["kidney_function"] == 90


def test_missing_parameter_raises_error():

    base_profile = {
        "age": 45
    }

    with pytest.raises(ValueError):
        generate_parameter_sweep(
            base_profile,
            "kidney_function",
            [90, 60, 30]
        )


def test_empty_values_raise_error():

    base_profile = {
        "age": 45,
        "kidney_function": 90
    }

    with pytest.raises(ValueError):
        generate_parameter_sweep(
            base_profile,
            "kidney_function",
            []
        )