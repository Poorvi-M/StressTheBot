from abc import ABC, abstractmethod

from app.llm.response_schema import LLMResponse


class BaseLLMClient(ABC):

    @abstractmethod
    def generate(
        self,
        scenario_id: str,
        prompt: str
    ) -> LLMResponse:
        pass