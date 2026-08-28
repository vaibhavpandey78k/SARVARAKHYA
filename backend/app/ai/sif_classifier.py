# Transparent baseline heuristic. This is NOT a calibrated probability.
HIGH_RISK_CUES = {
    "isolation", "lockout", "loto", "energized", "line of fire", "suspended load", "falling object",
    "confined space", "hot work", "gas test", "bypassed", "failed barrier", "missing guard", "permit not",
    "not verified", "not confirmed", "before isolation", "before electrical isolation", "exposed", "caught between", "crush zone", "pinch point"
}

NEGATIVE_CUES = {"training only", "planned drill", "no exposure", "fully compliant", "verified safe"}

def classify(text: str) -> dict:
    low = text.lower()
    hits = sorted({cue for cue in HIGH_RISK_CUES if cue in low})
    negatives = sorted({cue for cue in NEGATIVE_CUES if cue in low})
    score = min(1.0, 0.12 * len(hits) + (0.12 if "could" in low or "potential" in low else 0))
    if "before electrical isolation" in low or "before isolation" in low:
        score = max(score, 0.72)
    if negatives and not hits:
        score = 0.0
    if score >= 0.48:
        status, pred, conf = "sif-potential", True, "high" if score >= 0.72 else "medium"
    elif score >= 0.24:
        status, pred, conf = "uncertain", None, "medium"
    else:
        status, pred, conf = "non-sif-potential", False, "low"
    evidence = [f"risk cue: {h}" for h in hits]
    return {"sif_prediction": pred, "sif_status": status, "sif_score": round(score, 3), "sif_probability": None, "confidence": conf, "evidence": evidence}
