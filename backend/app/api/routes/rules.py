
from fastapi import APIRouter, HTTPException, Query

from app.rules.repository import (
    get_all_rules,
    get_rule_by_id
)


router = APIRouter(
    prefix="/api/rules",
    tags=["Clinical Rules"]
)


def serialize_rule(rule):
    """
    Convert a ClinicalRule into a JSON-compatible dictionary.
    Includes parameter definitions and source provenance.
    """
    return rule.model_dump(mode="json")


@router.get("/")
def fetch_rules(
    category: str | None = Query(default=None),
    status: str | None = Query(default=None)
):
    rules = get_all_rules()

    if category:
        rules = [
            rule for rule in rules
            if rule.category == category
        ]

    if status:
        rules = [
            rule for rule in rules
            if rule.status == status
        ]

    return {
        "total_rules": len(rules),
        "rules": [
            serialize_rule(rule)
            for rule in rules
        ]
    }


@router.get("/{rule_id}")
def fetch_rule(rule_id: str):
    rule = get_rule_by_id(rule_id)

    if rule is None:
        raise HTTPException(
            status_code=404,
            detail="Clinical rule not found"
        )

    return serialize_rule(rule)
