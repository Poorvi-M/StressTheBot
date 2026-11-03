import pytest

from app.llm.base import BaseLLMClient
from app.llm.response_schema import LLMResponse
from app.llm.runner import LLMRunner

from app.evaluation.evaluation_schema import EvaluationCheck
from app.evaluation.scenario_executor import execute_scenario


class MockLLMClient(BaseLLMClient):

    def generate(self, scenario_id, prompt):
        return LLMResponse(
            scenario_id=scenario_id,
            provider="mock",
            model="mock-model",
            prompt=prompt,
            response_text=(
                "Monitor renal function regularly. "
                "The medication should be used despite the warning."
            ),
            status="success"
        )


def test_execute_scenario_complete_workflow():

    scenario = {
        "scenario_id": "TEST001-S001",
        "rule_id": "TEST001",
        "patient_profile": {
            "age": 45,
            "kidney_function": 90
        }
    }

    template = (
        "A fictional patient aged {age} has a recorded "
        "kidney_function value of {kidney_function}."
    )

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    checks = [
        EvaluationCheck(
            rule_id="TEST001",
            prohibited_patterns=["used despite the warning"],
            severity="high"
        ),
        EvaluationCheck(
            rule_id="TEST002",
            required_patterns=["monitor renal function"],
            severity="medium"
        )
    ]

    result = execute_scenario(
        scenario=scenario,
        template=template,
        runner=runner,
        checks=checks
    )

    assert result["scenario_id"] == "TEST001-S001"
    assert result["rule_id"] == "TEST001"

    assert "45" in result["rendered_prompt"]
    assert "90" in result["rendered_prompt"]

    evaluation = result["evaluation"]

    assert evaluation["total_responses"] == 1
    assert evaluation["total_extracted"] == 1
    assert evaluation["total_evaluations"] == 2
    assert evaluation["total_errors"] == 0

    statuses = [
        item["status"]
        for item in evaluation["evaluation_results"]
    ]

    assert statuses == [
        "potential_violation",
        "no_detected_issue"
    ]


def test_execute_scenario_missing_id():

    scenario = {
        "rule_id": "TEST001",
        "patient_profile": {"age": 45}
    }

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    with pytest.raises(ValueError, match="Scenario ID"):
        execute_scenario(
            scenario=scenario,
            template="Patient age: {age}",
            runner=runner,
            checks=[]
        )


def test_execute_scenario_missing_profile():

    scenario = {
        "scenario_id": "TEST001-S001",
        "rule_id": "TEST001"
    }

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    with pytest.raises(ValueError, match="Patient profile"):
        execute_scenario(
            scenario=scenario,
            template="Patient age: {age}",
            runner=runner,
            checks=[]
        )


def test_execute_scenario_missing_template_field():

    scenario = {
        "scenario_id": "TEST001-S001",
        "rule_id": "TEST001",
        "patient_profile": {"age": 45}
    }

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    with pytest.raises(ValueError, match="missing"):
        execute_scenario(
            scenario=scenario,
            template="Patient age: {age}, kidney function: {kidney_function}",
            runner=runner,
            checks=[]
        )