import pytest

from app.llm.response_schema import LLMResponse
from app.response_extractor.extractor import extract_response


def make_response(text, status="success"):
    return LLMResponse(
        scenario_id="TEST001-S001",
        provider="groq",
        model="mock-model",
        prompt="Synthetic test prompt",
        response_text=text if status == "success" else None,
        status=status,
        error_message=None if status == "success" else "API error"
    )


def test_extracts_multiple_categories():
    response = make_response(
        "The medication recommendation requires further review. "
        "A contraindication warning should be considered. "
        "Monitor renal function regularly. "
        "An alternative medication may be considered. "
        "There is insufficient information to determine suitability."
    )

    result = extract_response(response)

    assert len(result.medication_recommendations) == 1
    assert len(result.contraindication_warnings) == 1
    assert len(result.monitoring_recommendations) == 1
    assert len(result.alternative_suggestions) == 1
    assert len(result.uncertainty_statements) == 1


def test_preserves_raw_response():
    text = "This is a synthetic test response."

    result = extract_response(make_response(text))

    assert result.raw_response == text


def test_empty_successful_response():
    result = extract_response(make_response(""))

    assert result.raw_response == ""
    assert result.safety_alerts == []


def test_rejects_failed_response():
    response = make_response("", status="error")

    with pytest.raises(ValueError, match="unsuccessful"):
        extract_response(response)