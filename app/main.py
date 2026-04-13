"""FastAPI scoring endpoint for lead conversion prediction."""

from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

ARTEFACTS = Path(__file__).resolve().parent / "artefacts"

# --- Pydantic models ---
class LeadInput(BaseModel):
    age: int = Field(ge=18, le=120)
    gender: str = Field(examples=["Male"])
    smoker: str = Field(examples=["no"])
    current_insurance: str = Field(examples=["no"])
    device_type: str = Field(examples=["Smartphone"])
    match_type: Optional[str] = Field(default=None, examples=["Exact"])
    cover_for: str = Field(examples=["Self"])
    verification_status: str = Field(examples=["verified"])
    keyword_group: str = Field(examples=["Brand: Bupa"])
    pc_area: str = Field(examples=["M"])

class ScoreOutput(BaseModel):
    conversion_probability: float
    risk_tier: str  # high / medium / low


# --- App lifespan: load model once ---
ml_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_state["model"] = joblib.load(ARTEFACTS / "model.joblib")
    ml_state["encoders"] = joblib.load(ARTEFACTS / "encoders.joblib")
    ml_state["features"] = joblib.load(ARTEFACTS / "feature_names.joblib")
    yield
    ml_state.clear()

app = FastAPI(
    title="LeadSense Scoring API",
    version="0.1.0",
    description="Score insurance leads by conversion probability.",
    lifespan=lifespan,
)


def _encode_input(lead: LeadInput) -> np.ndarray:
    """Convert a lead to a feature vector matching the trained model."""
    raw = {
        "age": lead.age,
        "gender": lead.gender,
        "smoker": lead.smoker,
        "current_insurance": lead.current_insurance,
        "device_type": lead.device_type,
        "match_type": str(lead.match_type),
        "cover_for": lead.cover_for,
        "verification_status": lead.verification_status,
        "keyword_group": lead.keyword_group,
        "pc_area": lead.pc_area,
    }
    encoded = []
    for feat in ml_state["features"]:
        val = raw[feat]
        if feat in ml_state["encoders"]:
            le = ml_state["encoders"][feat]
            if val in le.classes_:
                val = le.transform([val])[0]
            else:
                val = 0  # unseen category fallback
        encoded.append(val)
    return pd.DataFrame([encoded], columns=ml_state["features"])


@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": "model" in ml_state}


@app.post("/score", response_model=ScoreOutput)
async def score_lead(lead: LeadInput):
    X = _encode_input(lead)
    prob = float(ml_state["model"].predict_proba(X)[0, 1])
    tier = "high" if prob >= 0.08 else "medium" if prob >= 0.04 else "low"
    return ScoreOutput(conversion_probability=round(prob, 4), risk_tier=tier)
