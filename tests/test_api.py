"""Tests for the FastAPI scoring API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    """Spin up the app (loads model) and return a test client."""
    with TestClient(app) as c:
        yield c


VALID_LEAD = {
    "age": 35,
    "gender": "Male",
    "smoker": "no",
    "current_insurance": "no",
    "device_type": "Smartphone",
    "match_type": "Exact",
    "cover_for": "Self",
    "verification_status": "verified",
    "keyword_group": "Brand: Bupa",
    "pc_area": "M",
}


class TestHealth:
    def test_health_returns_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "ok"
        assert body["model_loaded"] is True


class TestScore:
    def test_score_returns_probability_and_tier(self, client):
        resp = client.post("/score", json=VALID_LEAD)
        assert resp.status_code == 200
        body = resp.json()
        assert 0.0 <= body["conversion_probability"] <= 1.0
        assert body["risk_tier"] in ("high", "medium", "low")

    def test_score_unseen_category_handled(self, client):
        """Unseen categorical values shouldn't crash the API."""
        lead = {**VALID_LEAD, "keyword_group": "UNKNOWN_KEYWORD"}
        resp = client.post("/score", json=lead)
        assert resp.status_code == 200
        assert 0.0 <= resp.json()["conversion_probability"] <= 1.0

    def test_score_missing_optional_field(self, client):
        """match_type is Optional — omitting it should still work."""
        lead = {k: v for k, v in VALID_LEAD.items() if k != "match_type"}
        resp = client.post("/score", json=lead)
        assert resp.status_code == 200

    def test_score_invalid_age_rejected(self, client):
        lead = {**VALID_LEAD, "age": 5}
        resp = client.post("/score", json=lead)
        assert resp.status_code == 422  # validation error

    def test_score_missing_required_field(self, client):
        lead = {k: v for k, v in VALID_LEAD.items() if k != "age"}
        resp = client.post("/score", json=lead)
        assert resp.status_code == 422

    def test_tier_thresholds(self, client):
        """Verify tier logic: high >= 0.08, medium >= 0.04, low < 0.04."""
        resp = client.post("/score", json=VALID_LEAD)
        body = resp.json()
        prob = body["conversion_probability"]
        expected = "high" if prob >= 0.08 else "medium" if prob >= 0.04 else "low"
        assert body["risk_tier"] == expected
