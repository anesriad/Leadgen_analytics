# App

Serving and UI layer for LeadSense.

## Components

| File | What it does |
|------|-------------|
| `main.py` | FastAPI scoring API — `/health` and `/score` endpoints |
| `dashboard.py` | Streamlit dashboard — KPIs, funnel, dimensional RPL, lead scorer |
| `simulate.py` | Generates synthetic leads from real distributions, optionally scores via API |
| `artefacts/` | Trained model, label encoders, feature names (joblib) |

## Running Locally

```bash
# 1. Start the scoring API
uvicorn app.main:app --port 8000

# 2. Start the dashboard (separate terminal)
streamlit run app/dashboard.py

# 3. Generate and score synthetic leads
python app/simulate.py -n 20 --score
```

## API Endpoints

- **GET /health** — returns `{"status": "ok", "model_loaded": true}`
- **POST /score** — accepts lead features, returns `{"conversion_probability": 0.31, "risk_tier": "high"}`
