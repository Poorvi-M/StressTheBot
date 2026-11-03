import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq, APIError

from app.llm.base import BaseLLMClient
from app.llm.response_schema import LLMResponse


# Load environment variables from backend/.env
BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BACKEND_DIR / ".env")


class GroqClient(BaseLLMClient):

    def __init__(self, model: str | None = None):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Check your backend/.env file."
            )

        self.model = model or os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        )

        self.client = Groq(api_key=api_key)

    def generate(
        self,
        scenario_id: str,
        prompt: str
    ) -> LLMResponse:

        try:
            result = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_text = (
                result.choices[0].message.content or ""
            )

            return LLMResponse(
                scenario_id=scenario_id,
                provider="groq",
                model=self.model,
                prompt=prompt,
                response_text=response_text,
                status="success"
            )

        except APIError as error:
            return LLMResponse(
                scenario_id=scenario_id,
                provider="groq",
                model=self.model,
                prompt=prompt,
                status="error",
                error_message=str(error)
            )