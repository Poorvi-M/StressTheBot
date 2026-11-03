from app.llm.runner import LLMRunner
from app.evaluation.evaluation_schema import EvaluationCheck
from app.evaluation.scenario_executor import execute_scenario


def execute_batch(
    scenarios: list[dict],
    template: str,
    runner: LLMRunner,
    checks: list[EvaluationCheck],
    providers: list[str] | None = None
) -> dict:
    """
    Execute multiple generated scenarios and collect their results.
    """

    if not scenarios:
        raise ValueError("Scenario batch cannot be empty")

    results = []
    execution_errors = []

    for scenario in scenarios:

        scenario_id = scenario.get("scenario_id", "unknown")

        try:
            result = execute_scenario(
                scenario=scenario,
                template=template,
                runner=runner,
                checks=checks,
                providers=providers
            )

            results.append(result)

        except Exception as error:
            execution_errors.append({
                "scenario_id": scenario_id,
                "error": str(error)
            })

    total_responses = sum(
        result["evaluation"]["total_responses"]
        for result in results
    )

    total_extracted = sum(
        result["evaluation"]["total_extracted"]
        for result in results
    )

    total_evaluations = sum(
        result["evaluation"]["total_evaluations"]
        for result in results
    )

    total_api_errors = sum(
        result["evaluation"]["total_errors"]
        for result in results
    )

    return {
        "total_scenarios": len(scenarios),
        "successful_scenarios": len(results),
        "failed_scenarios": len(execution_errors),
        "total_responses": total_responses,
        "total_extracted": total_extracted,
        "total_evaluations": total_evaluations,
        "total_api_errors": total_api_errors,
        "results": results,
        "execution_errors": execution_errors
    }