from app.risk_mapping.risk_summary import generate_risk_summary


def test_generate_risk_summary():

    records = [
        {
            "provider": "groq",
            "model": "mock-model",
            "rule_id": "RULE001",
            "severity": "high",
            "status": "potential_violation",
            "patient_parameters": {
                "kidney_function": 90
            }
        },
        {
            "provider": "groq",
            "model": "mock-model",
            "rule_id": "RULE001",
            "severity": "high",
            "status": "no_detected_issue",
            "patient_parameters": {
                "kidney_function": 60
            }
        },
        {
            "provider": "openai",
            "model": "another-model",
            "rule_id": "RULE002",
            "severity": "critical",
            "status": "missing_expected_behavior",
            "patient_parameters": {
                "kidney_function": 30
            }
        }
    ]

    result = generate_risk_summary(records)

    assert result["total_records"] == 3

    assert result["by_model"]["groq:mock-model"] == 2
    assert result["by_model"]["openai:another-model"] == 1

    assert result["by_rule"]["RULE001"] == 2
    assert result["by_rule"]["RULE002"] == 1

    assert result["by_severity"]["high"] == 2
    assert result["by_severity"]["critical"] == 1

    assert result["by_status"]["potential_violation"] == 1
    assert result["by_status"]["no_detected_issue"] == 1
    assert result["by_status"]["missing_expected_behavior"] == 1

    assert result["by_parameter"]["kidney_function"]["90"] == 1
    assert result["by_parameter"]["kidney_function"]["60"] == 1
    assert result["by_parameter"]["kidney_function"]["30"] == 1


def test_generate_empty_summary():

    result = generate_risk_summary([])

    assert result["total_records"] == 0
    assert result["by_model"] == {}
    assert result["by_rule"] == {}
    assert result["by_severity"] == {}
    assert result["by_status"] == {}
    assert result["by_parameter"] == {}