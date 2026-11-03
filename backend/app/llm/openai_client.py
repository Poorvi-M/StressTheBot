import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI, APIError

from app.llm.base import BaseLLMClient
from app.llm.response_schema import LLMResponse


# Load the .env file from the backend directory.
BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")


class OpenAIClient(BaseLLMClient):

    def __init__(self, model: str | None = None):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found. Check your backend/.env file."
            )

        self.model = model or os.getenv(
            "OPENAI_MODEL",
            "gpt-4.1-mini"
        )

        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        scenario_id: str,
        prompt: str
    ) -> LLMResponse:

        try:
            result = self.client.responses.create(
                model=self.model,
                input=prompt
            )

            return LLMResponse(
                scenario_id=scenario_id,
                provider="openai",
                model=self.model,
                prompt=prompt,
                response_text=result.output_text,
                status="success"
            )

        except APIError as error:
            return LLMResponse(
                scenario_id=scenario_id,
                provider="openai",
                model=self.model,
                prompt=prompt,
                status="error",
                error_message=str(error)
            )