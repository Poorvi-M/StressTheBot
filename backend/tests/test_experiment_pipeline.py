
from app.experiment.experiment_pipeline import run_experiment
from app.schemas.rule_schema import ClinicalRule
from app.llm.response_schema import LLMResponse
from app.llm.runner import LLMRunner
from app.evaluation.evaluation_schema import EvaluationCheck


class MockLLMClient:
    def generate(self, scenario_id: str, prompt: str) -> LLMResponse:
        return LLMResponse(
            scenario_id=scenario_id,
            provider="mock",
            model="mock-model",
            prompt=prompt,
            response_text="This is a dangerous instruction.",
            status="success"
        )


def create_test_rule():
    return ClinicalRule(
        rule_id="TEST001",
        title="Software testing rule",
        category="test",
        source_name="Software Testing Placeholder",
        source_url="https://example.com/test",
        source_excerpt="Placeholder content for testing.",

        applicability_conditions=[
            "Software testing only"
        ],
        expected_safe_behavior=[
            "Avoid the prohibited pattern"
        ],

        parameters=["age"],

        parameter_definitions=[
            {
                "name": "age",
                "data_type": "integer",
                "description": "Synthetic age used for software testing",
                "unit": "years",
                "required": True,
                "minimum": 18,
                "maximum": 100,
                "allowed_values": []
            }
        ],

        severity="high",
        severity_rationale="Placeholder severity for software testing.",
        status="draft",
        reviewed_by=None,
        reviewed_at=None,
        review_notes=None
    )


def test_run_experiment_end_to_end():
    rule = create_test_rule()

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    checks = [
        EvaluationCheck(
            rule_id="TEST001",
            prohibited_patterns=["dangerous instruction"],
            required_patterns=[],
            applicable=True,
            severity="high"
        )
    ]

    result = run_experiment(
        rule=rule,
        parameter_sets=[
            {"age": 45}
        ],
        template="Synthetic test profile. Age: {age}",
        runner=runner,
        checks=checks
    )

    assert result["experiment_status"] == "completed"
    assert result["generation"]["total_generated"] == 1

    assert result["batch_execution"]["successful_scenarios"] == 1

    assert result["risk_mapping"]["total_risk_records"] == 1

    risk_record = result["risk_mapping"]["risk_records"][0]

    assert risk_record["rule_id"] == "TEST001"
    assert risk_record["status"] == "potential_violation"
    assert risk_record["patient_parameters"]["age"] == 45

    assert result["risk_summary"]["total_records"] == 1


def test_run_experiment_with_no_valid_scenarios():
    rule = create_test_rule()

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    result = run_experiment(
        rule=rule,
        parameter_sets=[
            {}
        ],
        template="Synthetic test profile. Age: {age}",
        runner=runner,
        checks=[]
    )

    assert result["experiment_status"] == "no_valid_scenarios"
    assert result["generation"]["total_generated"] == 0
    assert result["generation"]["total_rejected"] == 1
    assert result["risk_mapping"]["total_risk_records"] == 0
