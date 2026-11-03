
from typing import Any

from app.schemas.rule_schema import ClinicalRule
from app.scenario_generator.generator import generate_scenarios
from app.evaluation.batch_executor import execute_batch
from app.risk_mapping.risk_mapper import map_batch_results
from app.risk_mapping.risk_summary import generate_risk_summary


def run_experiment(
    rule: ClinicalRule,
    parameter_sets: list[dict[str, Any]],
    template: str,
    runner,
    checks: list,
    parameter_constraints: dict[str, dict] | None = None,
    providers: list[str] | None = None
) -> dict:
    """
    Run a complete experiment:

    1. Generate and validate scenarios.
    2. Execute scenarios against selected LLMs.
    3. Evaluate model responses.
    4. Map evaluation results into risk records.
    5. Generate aggregate risk summaries.
    """

    # Step 1: Generate scenarios
    generated = generate_scenarios(
        rule=rule,
        parameter_sets=parameter_sets,
        parameter_constraints=parameter_constraints
    )

    scenarios = generated["scenarios"]

    if not scenarios:
        return {
            "rule_id": rule.rule_id,
            "generation": generated,
            "batch_execution": None,
            "risk_mapping": {
                "total_risk_records": 0,
                "total_mapping_errors": 0,
                "risk_records": [],
                "mapping_errors": []
            },
            "risk_summary": generate_risk_summary([]),
            "experiment_status": "no_valid_scenarios"
        }

    # Step 2: Execute scenarios and evaluate responses
    batch_result = execute_batch(
        scenarios=scenarios,
        template=template,
        runner=runner,
        checks=checks,
        providers=providers
    )

    # Step 3: Convert evaluation results into risk records
    risk_mapping = map_batch_results(batch_result)

    # Step 4: Aggregate risk records
    risk_summary = generate_risk_summary(
        risk_mapping["risk_records"]
    )

    # Step 5: Determine experiment status
    total_evaluations = batch_result["total_evaluations"]
    total_api_errors = batch_result["total_api_errors"]
    total_execution_errors = batch_result["failed_scenarios"]
    total_mapping_errors = risk_mapping["total_mapping_errors"]

    if total_evaluations == 0:
        experiment_status = "failed"

    elif (
        total_api_errors > 0
        or total_execution_errors > 0
        or total_mapping_errors > 0
    ):
        experiment_status = "partially_completed"

    else:
        experiment_status = "completed"

    return {
        "rule_id": rule.rule_id,
        "generation": generated,
        "batch_execution": batch_result,
        "risk_mapping": risk_mapping,
        "risk_summary": risk_summary,
        "experiment_status": experiment_status
    }
