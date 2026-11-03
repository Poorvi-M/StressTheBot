
import pytest
from pydantic import ValidationError

from app.schemas.rule_schema import ClinicalRule


def get_valid_rule():
    return {
        "rule_id": "TEST001",
        "title": "Sample rule for testing",
        "category": "medication_safety",
        "source_name": "Software Testing Placeholder",
        "source_url": "https://example.com/test-rule",
        "source_excerpt": "Placeholder text for testing.",
        "applicability_conditions": [
            "Testing condition"
        ],
        "expected_safe_behavior": [
            "Expected testing behaviour"
        ],
        "parameters": ["test_parameter"],
        "parameter_definitions": [
            {
                "name": "test_parameter",
                "data_type": "string",
                "description": "Test parameter used for schema validation",
                "unit": None,
                "required": True,
                "minimum": None,
                "maximum": None,
                "allowed_values": []
            }
        ],
        "severity": "low",
        "severity_rationale": "Placeholder severity for software testing.",
        "status": "draft",
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": None
    }


def test_valid_rule_is_accepted():
    rule = ClinicalRule.model_validate(get_valid_rule())

    assert rule.rule_id == "TEST001"
    assert rule.severity == "low"
    assert len(rule.parameter_definitions) == 1


def test_invalid_severity_is_rejected():
    rule_data = get_valid_rule()
    rule_data["severity"] = "extreme"

    with pytest.raises(ValidationError):
        ClinicalRule.model_validate(rule_data)


def test_missing_rule_id_is_rejected():
    rule_data = get_valid_rule()
    del rule_data["rule_id"]

    with pytest.raises(ValidationError):
        ClinicalRule.model_validate(rule_data)


def test_mismatched_parameter_definitions_are_rejected():
    rule_data = get_valid_rule()
    rule_data["parameter_definitions"] = []

    with pytest.raises(ValidationError):
        ClinicalRule.model_validate(rule_data)
