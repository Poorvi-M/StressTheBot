from app.rules.rule_loader import load_clinical_rules


def get_all_rules():
    return load_clinical_rules()


def get_rule_by_id(rule_id: str):

    rules = load_clinical_rules()

    for rule in rules:
        if rule.rule_id == rule_id:
            return rule

    return None


def get_rules_by_category(category: str):

    rules = load_clinical_rules()

    return [
        rule for rule in rules
        if rule.category == category
    ]