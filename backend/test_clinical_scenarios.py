from app.experiment import experiment_pipeline
from app.rules.repository import get_rule_by_id
from app.scenario_generator.generator import (
    generate_scenarios,
    generate_scenarios_from_sweep
)


def test_nsaid_scenarios():
    rule = get_rule_by_id("KDIGO-CKD-NSAID-001")

    parameter_sets = [
        {
            "ckd_status": "present",
            "nsaid_use_pattern": "chronic_indiscriminate_otc"
        },
        {
            "ckd_status": "present",
            "nsaid_use_pattern": "judicious_nephrologist_supervised"
        },
        {
            "ckd_status": "present",
            "nsaid_use_pattern": "not_using"
        }
    ]

    result = generate_scenarios(rule, parameter_sets)

    assert result["total_generated"] == 3
    assert result["total_rejected"] == 0

    print("\nNSAID scenarios:", result["scenarios"])


def test_herbal_scenarios():
    rule = get_rule_by_id("KDIGO-CKD-HERBAL-001")

    parameter_sets = [
        {
            "ckd_status": "present",
            "herbal_remedy_use": "currently_using",
            "volume_depletion": "present",
            "concurrent_illness": "absent",
            "concurrent_medication_use": "present"
        },
        {
            "ckd_status": "present",
            "herbal_remedy_use": "not_using",
            "volume_depletion": "absent",
            "concurrent_illness": "absent",
            "concurrent_medication_use": "absent"
        }
    ]

    result = generate_scenarios(rule, parameter_sets)

    assert result["total_generated"] == 2
    assert result["total_rejected"] == 0

    print("\nHerbal scenarios:", result["scenarios"])


def test_supplement_scenarios():
    rule = get_rule_by_id("KDIGO-CKD-SUPPLEMENT-001")

    parameter_sets = [
        {
            "ckd_status": "present",
            "supplement_use": "currently_using",
            "ingredient_identification": "unknown",
            "safety_information": "unavailable"
        },
        {
            "ckd_status": "present",
            "supplement_use": "considering_use",
            "ingredient_identification": "known",
            "safety_information": "available"
        }
    ]

    result = generate_scenarios(rule, parameter_sets)

    assert result["total_generated"] == 2
    assert result["total_rejected"] == 0

    print("\nSupplement scenarios:", result["scenarios"])


def test_invalid_scenario_is_rejected():
    rule = get_rule_by_id("KDIGO-CKD-NSAID-001")

    parameter_sets = [
        {
            "ckd_status": "present",
            "nsaid_use_pattern": "unsafe_value"
        }
    ]

    result = generate_scenarios(rule, parameter_sets)

    assert result["total_generated"] == 0
    assert result["total_rejected"] == 1

    print("\nRejected scenario:", result["rejected_scenarios"])


def test_nsaid_parameter_sweep():
    rule = get_rule_by_id("KDIGO-CKD-NSAID-001")

    base_profile = {
        "ckd_status": "present",
        "nsaid_use_pattern": "not_using"
    }

    values = [
        "not_using",
        "chronic_indiscriminate_otc",
        "judicious_nephrologist_supervised"
    ]

    result = generate_scenarios_from_sweep(
        rule=rule,
        base_profile=base_profile,
        parameter="nsaid_use_pattern",
        values=values
    )

    assert result["total_generated"] == 3
    assert result["total_rejected"] == 0
    assert result["sweep"]["parameter"] == "nsaid_use_pattern"

    print("\nSweep result:", result["scenarios"])

def setup_experiment_mocks(monkeypatch, total_evaluations, total_api_errors=0,
                           failed_scenarios=0, mapping_errors=0):

    monkeypatch.setattr(
        experiment_pipeline,
        "generate_scenarios",
        lambda **kwargs: {
            "scenarios": [{"scenario_id": "TEST-S001"}],
            "total_generated": 1,
            "total_rejected": 0
        }
    )

    monkeypatch.setattr(
        experiment_pipeline,
        "execute_batch",
        lambda **kwargs: {
            "total_scenarios": 1,
            "successful_scenarios": 1 - failed_scenarios,
            "failed_scenarios": failed_scenarios,
            "total_responses": total_evaluations + total_api_errors,
            "total_extracted": total_evaluations,
            "total_evaluations": total_evaluations,
            "total_api_errors": total_api_errors,
            "results": [],
            "execution_errors": []
        }
    )

    monkeypatch.setattr(
        experiment_pipeline,
        "map_batch_results",
        lambda batch_result: {
            "total_risk_records": total_evaluations,
            "total_mapping_errors": mapping_errors,
            "risk_records": [],
            "mapping_errors": []
        }
    )

    monkeypatch.setattr(
        experiment_pipeline,
        "generate_risk_summary",
        lambda records: {}
    )


def test_experiment_status_completed(monkeypatch):
    setup_experiment_mocks(
        monkeypatch,
        total_evaluations=2
    )

    rule = get_rule_by_id("KDIGO-CKD-NSAID-001")

    result = experiment_pipeline.run_experiment(
        rule=rule,
        parameter_sets=[],
        template="Test template",
        runner=None,
        checks=[]
    )

    assert result["experiment_status"] == "completed"


def test_experiment_status_partially_completed(monkeypatch):
    setup_experiment_mocks(
        monkeypatch,
        total_evaluations=1,
        total_api_errors=1
    )

    rule = get_rule_by_id("KDIGO-CKD-NSAID-001")

    result = experiment_pipeline.run_experiment(
        rule=rule,
        parameter_sets=[],
        template="Test template",
        runner=None,
        checks=[]
    )

    assert result["experiment_status"] == "partially_completed"


def test_experiment_status_failed(monkeypatch):
    setup_experiment_mocks(
        monkeypatch,
        total_evaluations=0,
        total_api_errors=2
    )

    rule = get_rule_by_id("KDIGO-CKD-NSAID-001")

    result = experiment_pipeline.run_experiment(
        rule=rule,
        parameter_sets=[],
        template="Test template",
        runner=None,
        checks=[]
    )

    assert result["experiment_status"] == "failed"


def test_experiment_status_no_valid_scenarios(monkeypatch):
    monkeypatch.setattr(
        experiment_pipeline,
        "generate_scenarios",
        lambda **kwargs: {
            "scenarios": [],
            "total_generated": 0,
            "total_rejected": 1
        }
    )

    rule = get_rule_by_id("KDIGO-CKD-NSAID-001")

    result = experiment_pipeline.run_experiment(
        rule=rule,
        parameter_sets=[],
        template="Test template",
        runner=None,
        checks=[]
    )

    assert result["experiment_status"] == "no_valid_scenarios"
    assert result["batch_execution"] is None
