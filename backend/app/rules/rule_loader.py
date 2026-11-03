import json
from pathlib import Path

from app.schemas.rule_schema import ClinicalRule


RULES_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "clinical_rules"
    / "clinical_rules.json"
)


def load_clinical_rules() -> list[ClinicalRule]:

    if not RULES_FILE.exists():
        raise FileNotFoundError(
            f"Clinical rules file not found: {RULES_FILE}"
        )

    with open(RULES_FILE, "r", encoding="utf-8") as file:
        rules_data = json.load(file)

    rules = [
        ClinicalRule.model_validate(rule)
        for rule in rules_data
    ]

    return rules