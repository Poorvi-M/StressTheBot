
from app.llm.base import BaseLLMClient
from app.llm.response_schema import LLMResponse


class LLMRunner:
    """
    Runs the same scenario against multiple LLM providers.
    """

    def __init__(self, clients: dict[str, BaseLLMClient]):

        if not clients:
            raise ValueError("At least one LLM client is required")

        self.clients = clients

    def run(
        self,
        scenario_id: str,
        prompt: str,
        providers: list[str] | None = None
    ) -> list[LLMResponse]:

        # None means use all configured providers.
        # An empty list means no providers were selected.
        selected_providers = (
            list(self.clients.keys())
            if providers is None
            else providers
        )

        if not selected_providers:
            raise ValueError("No providers selected")

        # Prevent accidentally querying the same provider twice.
        if len(selected_providers) != len(set(selected_providers)):
            raise ValueError("Duplicate providers are not allowed")

        results = []

        for provider in selected_providers:

            if provider not in self.clients:
                results.append(
                    LLMResponse(
                        scenario_id=scenario_id,
                        provider=provider,
                        model="unknown",
                        prompt=prompt,
                        status="error",
                        error_message=(
                            f"Provider '{provider}' is not configured"
                        )
                    )
                )
                continue

            client = self.clients[provider]

            try:
                response = client.generate(
                    scenario_id=scenario_id,
                    prompt=prompt
                )

                results.append(response)

            except Exception as error:

                results.append(
                    LLMResponse(
                        scenario_id=scenario_id,
                        provider=provider,
                        model="unknown",
                        prompt=prompt,
                        status="error",
                        error_message=str(error)
                    )
                )

        return results
