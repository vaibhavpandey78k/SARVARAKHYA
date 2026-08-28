# Configurable taxonomy. These rule names are examples explicitly referenced in the project brief.
RULE_PATTERNS = {
    "Energy Isolation": ["isolation", "isolated", "lockout", "lock out", "loto", "de-energ", "energized", "energy source", "electrical isolation"],
    "Hot Work": ["hot work", "welding", "weld", "cutting", "grinding", "spark", "ignition source"],
    "Confined Space": ["confined space", "tank entry", "vessel entry", "manhole", "gas test", "atmosphere test"],
    "Line of Fire": ["line of fire", "struck by", "caught between", "suspended load", "falling object", "crush zone", "pinch point"],
}

def map_rules(text: str) -> tuple[list[str], list[str]]:
    low = text.lower()
    rules, evidence = [], []
    for rule, patterns in RULE_PATTERNS.items():
        hits = [p for p in patterns if p in low]
        if hits:
            rules.append(rule)
            evidence.append(f"rule cue: {hits[0]}")
    return rules, evidence
