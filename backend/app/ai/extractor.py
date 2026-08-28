import re

ACTIVITY_PATTERNS = [
    "maintenance", "lifting", "hot work", "excavation", "electrical work", "transport", "inspection", "construction", "cleaning", "installation", "drilling"
]

LOCATION_PATTERNS = [
    "plant", "unit", "tank area", "workshop", "pump area", "pump", "maintenance area", "pipeline section", "warehouse", "site", "yard"
]

BARRIER_PATTERNS = {
    "isolation not verified": [
        "isolation not verified", "isolation was not confirmed", "before electrical isolation", "before isolation", "isolation not confirmed", "lockout verification was skipped"
    ],
    "failed isolation": ["failed isolation"],
    "missing isolation": ["missing isolation"],
    "guard missing": ["guard missing", "missing guard"],
    "inadequate permit": ["inadequate permit", "permit not obtained"],
    "gas testing failed": ["gas testing failed", "gas test not completed"],
    "line-of-fire exposure": ["line-of-fire exposure"],
    "barrier failed": ["barrier failed"],
}


def _find_phrase(text: str, patterns: list[str]) -> str | None:
    low = text.lower()
    for p in patterns:
        if p in low:
            return p
    return None


def _find_barrier(text: str) -> str | None:
    low = text.lower()
    for normalized, patterns in BARRIER_PATTERNS.items():
        if any(p in low for p in patterns):
            return normalized
    return None


def extract_entities(text: str) -> dict:
    activity = _find_phrase(text, ACTIVITY_PATTERNS)
    location = _find_phrase(text, LOCATION_PATTERNS)
    barrier = _find_barrier(text)
    evidence = []
    for value, label in [(activity, "activity"), (location, "location"), (barrier, "barrier")]:
        if value:
            evidence.append(f"{label}: {value}")
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    cue_words = ["isolation", "barrier", "permit", "line of fire", "confined", "hot work", "suspended", "gas test", "exposed"]
    sentence = next((s.strip() for s in sentences if any(c in s.lower() for c in cue_words)), None)
    if sentence:
        evidence.append(sentence[:500])
    return {"activity": activity, "location": location, "barrier_failure": barrier, "evidence": evidence}
