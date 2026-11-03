from app.llm.base import BaseLLMClient
from app.llm.response_schema import LLMResponse
from app.llm.runner import LLMRunner

from app.response_extractor.pipeline import (
    run_extraction_pipeline
)


class MockLLMClient(BaseLLMClient):

    def generate(self, scenario_id, prompt):
        return LLMResponse(
            scenario_id=scenario_id,
            provider="mock",
            model="mock-model",
            prompt=prompt,
            response_text=(
                "A contraindication warning should be considered. "
                "Monitor renal function regularly. "
                "There is insufficient information to determine suitability."
            ),
            status="success"
        )


def test_pipeline_runs_and_extracts_response():

    runner = LLMRunner({
        "mock": MockLLMClient()
    })

    result = run_extraction_pipeline(
        runner=runner,
        scenario_id="TEST001-S001",
        prompt="Synthetic patient scenario"
    )

    assert result["total_responses"] == 1
    assert result["total_extracted"] == 1
    assert result["total_errors"] == 0

    extracted = result["extracted_results"][0]

    assert len(extracted["contraindication_warnings"]) == 1
    assert len(extracted["monitoring_recommendations"]) == 1
    assert len(extracted["uncertainty_statements"]) == 1