from collections import Counter, defaultdict


def generate_risk_summary(risk_records: list[dict]) -> dict:
    """
    Aggregate risk records by model, rule, severity,
    evaluation status, and patient parameter values.
    """

    by_model = Counter()
    by_rule = Counter()
    by_severity = Counter()
    by_status = Counter()

    parameter_breakdown = defaultdict(Counter)

    for record in risk_records:

        model_key = f"{record['provider']}:{record['model']}"

        by_model[model_key] += 1
        by_rule[record["rule_id"]] += 1
        by_severity[record["severity"]] += 1
        by_status[record["status"]] += 1

        for parameter, value in record.get(
            "patient_parameters", {}
        ).items():

            parameter_breakdown[parameter][str(value)] += 1

    return {
        "total_records": len(risk_records),
        "by_model": dict(by_model),
        "by_rule": dict(by_rule),
        "by_severity": dict(by_severity),
        "by_status": dict(by_status),
        "by_parameter": {
            parameter: dict(values)
            for parameter, values in parameter_breakdown.items()
        }
    }