import pytest

from app.scenario_generator.renderer import render_scenario


def test_render_scenario_success():
    patient_profile = {
        "age": 45,
        "kidney_function": 90
    }

    template = (
        "A patient aged {age} has a recorded "
        "kidney_function value of {kidney_function}."
    )

    result = render_scenario(patient_profile, template)

    assert result == (
        "A patient aged 45 has a recorded "
        "kidney_function value of 90."
    )


def test_render_scenario_missing_field():
    patient_profile = {"age": 45}

    template = "A patient aged {age} has value {kidney_function}."

    with pytest.raises(ValueError, match="missing"):
        render_scenario(patient_profile, template)


def test_render_scenario_empty_template():
    with pytest.raises(ValueError, match="cannot be empty"):
        render_scenario({"age": 45}, "")


def test_render_scenario_empty_profile():
    with pytest.raises(ValueError, match="cannot be empty"):
        render_scenario({}, "A patient aged {age}.")


def test_render_scenario_rejects_format_specification():
    patient_profile = {"age": 45}

    with pytest.raises(ValueError, match="Format specifications"):
        render_scenario(patient_profile, "Patient age: {age:.2f}")