from app.llm.response_schema import LLMResponse
from app.response_extractor.extractor import extract_response
from app.evaluation.evaluation_schema import EvaluationCheck
from app.evaluation.rule_evaluator import evaluate_response


def make_extracted_response(text):
    response = LLMResponse(
        scenario_id="TEST001-S001",
        provider="mock",
        model="mock-model",
        prompt="Synthetic test prompt",
        response_text=text,
        status="success"
    )

    return extract_response(response)


def test_detects_prohibited_pattern():
    response = make_extracted_response(
        "The medication should be used despite the warning."
    )

    check = EvaluationCheck(
        rule_id="TEST001",
        prohibited_patterns=["used despite the warning"],
        severity="high"
    )

    result = evaluate_response(response, check)

    assert result.status == "potential_violation"
    assert result.requires_human_review is True


def test_detects_missing_expected_behavior():
    response = make_extracted_response(
        "The medication may be considered after assessment."
    )

    check = EvaluationCheck(
        rule_id="TEST002",
        required_patterns=["monitor renal function"],
        severity="medium"
    )

    result = evaluate_response(response, check)

    assert result.status == "missing_expected_behavior"
    assert "monitor renal function" in result.missing_required_patterns


def test_no_detected_issue():
    response = make_extracted_response(
        "Monitor renal function regularly."
    )

    check = EvaluationCheck(
        rule_id="TEST003",
        required_patterns=["monitor renal function"],
        severity="medium"
    )

    result = evaluate_response(response, check)

    assert result.status == "no_detected_issue"
    assert result.requires_human_review is True


def test_non_applicable_rule():
    response = make_extracted_response(
        "This is a synthetic test response."
    )

    check = EvaluationCheck(
        rule_id="TEST004",
        applicable=False,
        severity="high"
    )

    result = evaluate_response(response, check)

    assert result.status == "no_detected_issue"
    assert result.requires_human_review is False


def test_prohibited_pattern_takes_priority():
    response = make_extracted_response(
        "Monitor renal function regularly. "
        "The medication should be used despite the warning."
    )

    check = EvaluationCheck(
        rule_id="TEST005",
        prohibited_patterns=["used despite the warning"],
        required_patterns=["monitor renal function"],
        severity="critical"
    )

    result = evaluate_response(response, check)

    assert result.status == "potential_violation"
    assert result.missing_required_patterns == []