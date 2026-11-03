from app.scenario_generator.renderer import render_scenario
from app.llm.runner import LLMRunner
from app.evaluation.evaluation_schema import EvaluationCheck
from app.evaluation.pipeline import run_evaluation_pipeline


def execute_scenario(
    scenario: dict,
    template: str,
    runner: LLMRunner,
    checks: list[EvaluationCheck],
    providers: list[str] | None = None
) -> dict:
    """
    Execute one generated scenario through the complete
    LLM evaluation workflow.
    """

    # Step 1: Validate the scenario structure.
    if "scenario_id" not in scenario:
        raise ValueError("Scenario ID is missing")

    if "patient_profile" not in scenario:
        raise ValueError("Patient profile is missing")

    scenario_id = scenario["scenario_id"]
    patient_profile = scenario["patient_profile"]

    # Step 2: Render the patient profile into a prompt.
    prompt = render_scenario(
        patient_profile=patient_profile,
        template=template
    )

    # Step 3: Run the LLM and evaluation pipeline.
    evaluation = run_evaluation_pipeline(
        runner=runner,
        scenario_id=scenario_id,
        prompt=prompt,
        checks=checks,
        providers=providers
    )

    # Step 4: Return the complete scenario-level result.
    return {
        "scenario_id": scenario_id,
        "rule_id": scenario.get("rule_id"),
        "patient_profile": patient_profile,
        "rendered_prompt": prompt,
        "evaluation": evaluation
    }