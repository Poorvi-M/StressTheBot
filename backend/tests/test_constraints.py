from app.scenario_generator.constraints import validate_parameters


def test_valid_parameters():

    parameters = {
        "age": 45,
        "kidney_function": 60
    }

    required = ["age", "kidney_function"]

    constraints = {
        "age": {"min": 18, "max": 100},
        "kidney_function": {"min": 0, "max": 120}
    }

    is_valid, errors = validate_parameters(
        parameters,
        required,
        constraints
    )

    assert is_valid is True
    assert errors == []


def test_invalid_parameters():

    parameters = {
        "age": 15
    }

    required = ["age", "kidney_function"]

    constraints = {
        "age": {"min": 18, "max": 100}
    }

    is_valid, errors = validate_parameters(
        parameters,
        required,
        constraints
    )

    assert is_valid is False
    assert len(errors) == 2