from app.ai.sif_classifier import classify
from app.ai.rules import map_rules
from app.ai.extractor import extract_entities

class BaselineAnalyzer:
    analysis_type = "baseline"
    model_version = "baseline-v1"

    def analyze(self, report) -> dict:
        text = report.final_narrative
        result = classify(text)
        entities = extract_entities(text)
        rules, rule_evidence = map_rules(text)
        result.update(entities)
        result["life_saving_rules"] = rules
        result["evidence"] = result["evidence"] + rule_evidence
        return result

analyzer = BaselineAnalyzer()
