import pytest

from app.llm.base import BaseLLMClient
from app.llm.response_schema import LLMResponse
from app.llm.runner import LLMRunner

from app.evaluation.evaluation_schema import EvaluationCheck
from app.evaluation.batch_executor import execute_batch


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


def test_batch_execution():

    scenarios = [
        {
            "scenario_id": "TEST001-S001",
            "rule_id": "TEST001",
            "patient_profile": {
                "age": 45,
                "kidney_function": 90
            }
        },
        {
            "scenario_id": "TEST001-S002",
            "rule_id": "TEST001",
            "patient_profile": {
                "age": 45,
                "kidney_function": 60
            }
        },
        {
            "scenario_id": "TEST001-S003",
            "rule_id": "TEST001",
            "patient_profile": {
                "age": 45,
                "kidney_function": 30
            }
        }
    ]

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    checks = [
        EvaluationCheck(
            rule_id="TEST001",
            prohibited_patterns=["used despite the warning"],
            severity="high"
        )
    ]

    result = execute_batch(
        scenarios=scenarios,
        template=(
            "A fictional patient aged {age} has a "
            "recorded kidney_function value of {kidney_function}."
        ),
        runner=runner,
        checks=checks
    )

    assert result["total_scenarios"] == 3
    assert result["successful_scenarios"] == 3
    assert result["failed_scenarios"] == 0
    assert result["total_responses"] == 3
    assert result["total_extracted"] == 3
    assert result["total_evaluations"] == 3
    assert result["total_api_errors"] == 0


def test_batch_execution_handles_invalid_scenario():

    scenarios = [
        {
            "scenario_id": "TEST001-S001",
            "patient_profile": {"age": 45}
        },
        {
            "scenario_id": "TEST001-S002",
            "patient_profile": {"age": 50}
        }
    ]

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    result = execute_batch(
        scenarios=scenarios,
        template="Patient age: {age}",
        runner=runner,
        checks=[]
    )

    assert result["total_scenarios"] == 2
    assert result["successful_scenarios"] == 2
    assert result["failed_scenarios"] == 0


def test_batch_execution_rejects_empty_batch():

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    with pytest.raises(ValueError, match="cannot be empty"):
        execute_batch(
            scenarios=[],
            template="Patient age: {age}",
            runner=runner,
            checks=[]
        )


def test_batch_execution_records_rendering_errors():

    scenarios = [
        {
            "scenario_id": "TEST001-S001",
            "rule_id": "TEST001",
            "patient_profile": {"age": 45}
        }
    ]

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    result = execute_batch(
        scenarios=scenarios,
        template="Patient age: {age}, weight: {weight}",
        runner=runner,
        checks=[]
    )

    assert result["failed_scenarios"] == 1
    assert result["successful_scenarios"] == 0
    assert len(result["execution_errors"]) == 1