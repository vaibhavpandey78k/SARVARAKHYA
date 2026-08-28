import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine
from app.models import Report, Prediction, HumanReview  # noqa: F401

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_get_analyze():
    payload = {"report_text": "Technician entered the maintenance area before electrical isolation was confirmed.", "event_date": "2026-08-25", "site": "Plant A"}
    r = client.post("/api/reports", json=payload)
    assert r.status_code == 201
    rid = r.json()["id"]
    r = client.get(f"/api/reports/{rid}")
    assert r.status_code == 200
    r = client.post(f"/api/reports/{rid}/analyze")
    assert r.status_code == 200
    body = r.json()
    assert body["analysis_type"] == "baseline"
    assert body["model_version"] == "baseline-v1"
    assert "Energy Isolation" in body["life_saving_rules"]
    assert body["sif_status"] == "sif-potential"

def test_invalid_report():
    r = client.post("/api/reports", json={"report_text": "x"})
    assert r.status_code == 422
