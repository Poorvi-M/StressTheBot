from types import SimpleNamespace

from app.rules import repository


def test_get_all_rules(monkeypatch):

    sample_rules = [
        SimpleNamespace(rule_id="TEST001"),
        SimpleNamespace(rule_id="TEST002")
    ]

    monkeypatch.setattr(
        repository,
        "load_clinical_rules",
        lambda: sample_rules
    )

    rules = repository.get_all_rules()

    assert len(rules) == 2


def test_get_rule_by_id(monkeypatch):

    sample_rules = [
        SimpleNamespace(rule_id="TEST001"),
        SimpleNamespace(rule_id="TEST002")
    ]

    monkeypatch.setattr(
        repository,
        "load_clinical_rules",
        lambda: sample_rules
    )

    rule = repository.get_rule_by_id("TEST002")

    assert rule.rule_id == "TEST002"


def test_missing_rule_returns_none(monkeypatch):

    monkeypatch.setattr(
        repository,
        "load_clinical_rules",
        lambda: []
    )

    rule = repository.get_rule_by_id("UNKNOWN")

    assert rule is None
def test_get_rules_by_category(monkeypatch):

    sample_rules = [
        SimpleNamespace(
            rule_id="TEST001",
            category="medication_safety"
        ),
        SimpleNamespace(
            rule_id="TEST002",
            category="diagnostic_safety"
        ),
        SimpleNamespace(
            rule_id="TEST003",
            category="medication_safety"
        )
    ]

    monkeypatch.setattr(
        repository,
        "load_clinical_rules",
        lambda: sample_rules
    )

    rules = repository.get_rules_by_category(
        "medication_safety"
    )

    assert len(rules) == 2
    assert all(
        rule.category == "medication_safety"
        for rule in rules
    )