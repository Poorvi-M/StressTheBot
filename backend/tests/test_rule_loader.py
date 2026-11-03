
import json

import pytest

from app.rules import rule_loader


def test_loader_reads_valid_rules(tmp_path, monkeypatch):
    test_file = tmp_path / "clinical_rules.json"

    sample_rule = {
        "rule_id": "TEST001",
        "title": "Sample rule",
        "category": "medication_safety",
        "source_name": "Software Testing Placeholder",
        "source_url": "https://example.com/test-rule",
        "source_excerpt": "Placeholder testing content.",
        "source_publication_date": None,
        "source_version": None,
        "source_section": None,
        "source_page": None,
        "applicability_conditions": [
            "Testing condition"
        ],
        "expected_safe_behavior": [
            "Expected safe behaviour"
        ],
        "parameters": ["test_parameter"],
        "parameter_definitions": [
            {
                "name": "test_parameter",
                "data_type": "string",
                "description": "Placeholder parameter used for testing",
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

    test_file.write_text(
        json.dumps([sample_rule]),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        rule_loader,
        "RULES_FILE",
        test_file
    )

    rules = rule_loader.load_clinical_rules()

    assert len(rules) == 1
    assert rules[0].rule_id == "TEST001"
    assert rules[0].status == "draft"
    assert len(rules[0].parameter_definitions) == 1


def test_loader_returns_empty_list(tmp_path, monkeypatch):
    test_file = tmp_path / "clinical_rules.json"
    test_file.write_text("[]", encoding="utf-8")

    monkeypatch.setattr(
        rule_loader,
        "RULES_FILE",
        test_file
    )

    rules = rule_loader.load_clinical_rules()

    assert rules == []


def test_loader_rejects_invalid_json_rule(tmp_path, monkeypatch):
    test_file = tmp_path / "clinical_rules.json"

    invalid_rule = {
        "rule_id": "TEST002",
        "title": "Invalid rule",
        "source_name": "Testing",
        "source_url": "https://example.com/test",
        "source_excerpt": "Test",
        "applicability_conditions": ["Test"],
        "expected_safe_behavior": ["Test"],
        "parameters": [],
        "parameter_definitions": [],
        "severity": "extreme",
        "status": "draft"
    }

    test_file.write_text(
        json.dumps([invalid_rule]),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        rule_loader,
        "RULES_FILE",
        test_file
    )

    with pytest.raises(Exception):
        rule_loader.load_clinical_rules()
