import pytest

from app.llm.base import BaseLLMClient
from app.llm.runner import LLMRunner
from app.llm.response_schema import LLMResponse


class MockLLMClient(BaseLLMClient):

    def __init__(self, provider, response_text="Mock response"):
        self.provider = provider
        self.response_text = response_text

    def generate(self, scenario_id, prompt):
        return LLMResponse(
            scenario_id=scenario_id,
            provider=self.provider,
            model="mock-model",
            prompt=prompt,
            response_text=self.response_text,
            status="success"
        )


class FailingLLMClient(BaseLLMClient):

    def generate(self, scenario_id, prompt):
        raise RuntimeError("Simulated provider failure")


def test_runner_executes_multiple_providers():
    clients = {
        "groq": MockLLMClient("groq", "Groq response"),
        "openai": MockLLMClient("openai", "OpenAI response")
    }

    runner = LLMRunner(clients)

    results = runner.run(
        scenario_id="TEST001-S001",
        prompt="Synthetic test prompt"
    )

    assert len(results) == 2
    assert results[0].provider == "groq"
    assert results[1].provider == "openai"
    assert all(result.status == "success" for result in results)


def test_runner_can_select_one_provider():
    clients = {
        "groq": MockLLMClient("groq"),
        "openai": MockLLMClient("openai")
    }

    runner = LLMRunner(clients)

    results = runner.run(
        scenario_id="TEST001-S001",
        prompt="Test prompt",
        providers=["groq"]
    )

    assert len(results) == 1
    assert results[0].provider == "groq"


def test_runner_handles_unknown_provider():
    clients = {
        "groq": MockLLMClient("groq")
    }

    runner = LLMRunner(clients)

    results = runner.run(
        scenario_id="TEST001-S001",
        prompt="Test prompt",
        providers=["gemini"]
    )

    assert len(results) == 1
    assert results[0].provider == "gemini"
    assert results[0].status == "error"
    assert "not configured" in results[0].error_message


def test_runner_handles_provider_failure():
    clients = {
        "groq": FailingLLMClient()
    }

    runner = LLMRunner(clients)

    results = runner.run(
        scenario_id="TEST001-S001",
        prompt="Test prompt"
    )

    assert len(results) == 1
    assert results[0].status == "error"
    assert "Simulated provider failure" in results[0].error_message


def test_runner_rejects_empty_client_registry():
    with pytest.raises(ValueError, match="At least one"):
        LLMRunner({})