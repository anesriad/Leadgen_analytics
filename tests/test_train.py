"""Tests for the training pipeline."""

import joblib
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARTEFACTS = PROJECT_ROOT / "app" / "artefacts"


class TestArtefacts:
    """Verify that train.py produced valid artefacts."""

    def test_model_exists(self):
        assert (ARTEFACTS / "model.joblib").exists()

    def test_encoders_exist(self):
        assert (ARTEFACTS / "encoders.joblib").exists()

    def test_feature_names_exist(self):
        assert (ARTEFACTS / "feature_names.joblib").exists()

    def test_model_has_predict_proba(self):
        model = joblib.load(ARTEFACTS / "model.joblib")
        assert hasattr(model, "predict_proba")

    def test_encoders_cover_expected_columns(self):
        encoders = joblib.load(ARTEFACTS / "encoders.joblib")
        expected = {
            "gender", "smoker", "current_insurance", "device_type",
            "match_type", "cover_for", "verification_status",
            "keyword_group", "pc_area",
        }
        assert set(encoders.keys()) == expected

    def test_feature_names_order(self):
        features = joblib.load(ARTEFACTS / "feature_names.joblib")
        assert features[0] == "age"  # numeric first
        assert len(features) == 10
