from typing import Literal
from pydantic import BaseModel


class LLMResponse(BaseModel):
    scenario_id: str
    provider: str
    model: str
    prompt: str
    response_text: str | None = None
    status: Literal["success", "error"]
    error_message: str | None = None