from app.llm.runner import LLMRunner
from app.response_extractor.extractor import extract_response


def run_extraction_pipeline(
    runner: LLMRunner,
    scenario_id: str,
    prompt: str,
    providers: list[str] | None = None
) -> dict:

    # Step 1: Query the selected LLM providers.
    responses = runner.run(
        scenario_id=scenario_id,
        prompt=prompt,
        providers=providers
    )

    # Step 2: Extract information from successful responses.
    extracted_results = []
    extraction_errors = []

    for response in responses:

        if response.status != "success":
            extraction_errors.append({
                "provider": response.provider,
                "error": response.error_message
            })
            continue

        try:
            extracted = extract_response(response)
            extracted_results.append(extracted.model_dump())

        except Exception as error:
            extraction_errors.append({
                "provider": response.provider,
                "error": str(error)
            })

    return {
        "scenario_id": scenario_id,
        "total_responses": len(responses),
        "total_extracted": len(extracted_results),
        "total_errors": len(extraction_errors),
        "extracted_results": extracted_results,
        "extraction_errors": extraction_errors
    }