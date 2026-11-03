
import re

from app.llm.response_schema import LLMResponse
from app.response_extractor.extraction_schema import (
    ExtractedResponse,
    SafetyObservation
)


SECTION_PATTERNS = {
    "medication_recommendations": [
        r"medication recommendation",
        r"recommended medication",
        r"dosing recommendation",
        r"\bprescribe\b",
    ],
    "contraindication_warnings": [
        r"\bcontraindication\b",
        r"\bcontraindicated\b",
        r"\bshould not be used\b",
        r"\bmust not be used\b",
    ],
    "safety_alerts": [
        r"\bsafety alert\b",
        r"\bwarning\b",
        r"\badverse effect\b",
        r"\bdrug interaction\b",
        r"\bkidney damage\b",
        r"\bnephrotoxicity\b",
        r"\bkidney failure\b",
    ],
    "monitoring_recommendations": [
        r"\bmonitoring\b",
        r"\bmonitor\b",
        r"\brepeat lab\b",
        r"\blaboratory test\b",
        r"\btherapeutic drug monitoring\b",
    ],
    "alternative_suggestions": [
        r"\balternative\b",
        r"\bsubstitute\b",
        r"\breplacement medication\b",
    ],
    "rationale": [
        r"\brationale\b",
        r"\bbecause\b",
        r"\bjustification\b",
        r"\breasoning\b",
    ],
    "uncertainty_statements": [
        r"\buncertain\b",
        r"\binsufficient information\b",
        r"\bcannot determine\b",
        r"\badditional information\b",
        r"\bunknown\b",
    ],
}


SAFETY_OBSERVATION_PATTERNS = {
    "medication_safety": [
        r"\bNSAID\b",
        r"\bnonsteroidal anti-inflammatory\b",
        r"\bmedication safety\b",
    ],
    "kidney_risk": [
        r"\bkidney risk\b",
        r"\bkidney damage\b",
        r"\bkidney failure\b",
        r"\bnephrotoxicity\b",
        r"\brenal function\b",
    ],
    "herbal_remedy_safety": [
        r"\bherbal remed(?:y|ies)\b",
        r"\bherbal supplement\b",
        r"\bnatural compound\b",
    ],
    "supplement_safety": [
        r"\bdietary supplement\b",
        r"\bsupplement safety\b",
        r"\bsupplement ingredients\b",
    ],
    "monitoring": [
        r"\bmonitor\b",
        r"\bmonitoring\b",
        r"\bfollow-up testing\b",
    ],
    "contraindication": [
        r"\bcontraindicated\b",
        r"\bcontraindication\b",
        r"\bshould not be used\b",
    ],
    "uncertainty": [
        r"\buncertain\b",
        r"\bunknown\b",
        r"\binsufficient information\b",
        r"\bcannot determine\b",
    ],
}


def _split_sentences(text: str) -> list[str]:
    """
    Split a response into non-empty sentences.
    """

    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if sentence.strip()
    ]


def _matches_any(sentence: str, patterns: list[str]) -> bool:
    """
    Check whether a sentence matches at least one pattern.
    """

    return any(
        re.search(pattern, sentence, re.IGNORECASE)
        for pattern in patterns
    )


def _extract_safety_observations(
    sentences: list[str]
) -> list[SafetyObservation]:

    observations = []

    for sentence in sentences:

        for category, patterns in SAFETY_OBSERVATION_PATTERNS.items():

            if _matches_any(sentence, patterns):

                observations.append(
                    SafetyObservation(
                        category=category,
                        statement=sentence,
                        evidence_text=sentence,
                        explicitly_stated=True
                    )
                )

    return observations


def extract_response(
    response: LLMResponse
) -> ExtractedResponse:

    if response.status != "success":
        raise ValueError(
            "Cannot extract information from an unsuccessful response"
        )

    if not response.response_text or not response.response_text.strip():
        return ExtractedResponse(
            scenario_id=response.scenario_id,
            provider=response.provider,
            model=response.model,
            raw_response=response.response_text or ""
        )

    text = response.response_text

    extracted = {
        field: []
        for field in SECTION_PATTERNS
    }

    sentences = _split_sentences(text)

    for sentence in sentences:

        for field, patterns in SECTION_PATTERNS.items():

            if _matches_any(sentence, patterns):
                extracted[field].append(sentence)

    safety_observations = _extract_safety_observations(sentences)

    return ExtractedResponse(
        scenario_id=response.scenario_id,
        provider=response.provider,
        model=response.model,
        raw_response=text,
        safety_observations=safety_observations,
        **extracted
    )