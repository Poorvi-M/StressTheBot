
from app.risk_mapping.risk_schema import RiskRecord


def map_batch_results(batch_result: dict) -> dict:
    """
    Convert batch evaluation results into structured risk records.
    """

    risk_records = []
    mapping_errors = []

    for scenario_result in batch_result.get("results", []):

        scenario_id = scenario_result.get("scenario_id", "unknown")

        patient_parameters = scenario_result.get(
            "patient_profile", {}
        )

        evaluation = scenario_result.get("evaluation", {})

        for item in evaluation.get("evaluation_results", []):

            try:
                explanation = item["explanation"]

                # Preserve evidence candidates included by the evaluator.
                evidence = []

                marker = "Extracted evidence candidates: "

                if marker in explanation:
                    evidence_text = explanation.split(marker, 1)[1]

                    # Keep the original evidence representation as text.
                    evidence.append({
                        "source": "response_extractor",
                        "details": evidence_text
                    })

                record = RiskRecord(
                    scenario_id=scenario_id,
                    provider=item["provider"],
                    model=item["model"],
                    rule_id=item["rule_id"],
                    status=item["status"],
                    severity=item["severity"],
                    patient_parameters=patient_parameters,
                    matched_prohibited_patterns=item.get(
                        "matched_prohibited_patterns", []
                    ),
                    missing_required_patterns=item.get(
                        "missing_required_patterns", []
                    ),
                    evidence=evidence,
                    explanation=explanation,
                    requires_human_review=item.get(
                        "requires_human_review", True
                    )
                )

                risk_records.append(record.model_dump())

            except Exception as error:
                mapping_errors.append({
                    "scenario_id": scenario_id,
                    "error": str(error)
                })

    return {
        "total_risk_records": len(risk_records),
        "total_mapping_errors": len(mapping_errors),
        "risk_records": risk_records,
        "mapping_errors": mapping_errors
    }
