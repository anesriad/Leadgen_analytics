# Lead Acquisition Profitability System

An end-to-end ML and analytics project focused on insurance lead generation. Analyses lead profitability, predicts conversion probability, and helps optimize marketing spend.

## Architecture

```
Insurance Leads CSV ──┐
(anonymized)          ├──→ Data Mart ──→ Feature Pipeline ──→ ML Models ──→ FastAPI ──→ Streamlit Dashboard
                      │    (weekly KPIs)  (conversion/value)                              
Synthetic Spend ──────┘                                                       ↕
(marketing costs)                                                     A/B Testing
```

### Data Flow
1. **Raw** — anonymized lead CSV + synthetic spend → `data/raw/`
2. **Staging** — cleaned, standardized, validated → `data/staging/`
3. **Mart** — aggregated with KPIs (RPL, CAC, ROAS) → `data/mart/`
4. **Model** — trained models tracked in MLflow
5. **Serving** — FastAPI prediction endpoint + Streamlit UI

## Business Context

We pay **£55 per lead** (`COST_PER_LEAD`). The core question: **which lead segments are profitable and which are losing money?**

Key metrics:
- **RPL** — Revenue Per Lead (premium ÷ leads)
- **Net/Lead** — RPL minus cost (£55)
- **CAC** — Cost to Acquire a Conversion

## Project Structure

```
├── notebooks/          # Jupyter notebooks (01-07, run in order)
├── data/
│   ├── raw/            # Original data (never modified)
│   ├── staging/        # Cleaned and standardized
│   └── mart/           # Analytics-ready joined tables
├── src/
│   └── models/train.py  # Training script → saves to app/artefacts/
├── app/
│   ├── main.py          # FastAPI scoring API
│   ├── dashboard.py     # Streamlit dashboard
│   ├── simulate.py      # Synthetic lead generator
│   └── artefacts/       # Saved model, encoders, features
├── tests/              # 13 tests (API + artefact validation)
├── configs/            # Settings and parameters
└── Dockerfile
```

## Progress

| Phase | Notebook | Status |
|-------|----------|--------|
| 0. Dataset Prep (anonymize) | `00_dataset_prep.ipynb` | Done |
| 1. Data Fetch | `01_data_fetch.ipynb` | Done |
| 2. Clean & Validate | `02_clean_and_validate.ipynb` | Done |
| 3. EDA — Lead Profitability | `03_eda_leads.ipynb` | Done |
| 4. Hypothesis Testing | `04_hypothesis_testing.ipynb` | Done |
| 5. ML Experiments | `05_modeling.ipynb` | Done |
| 6. Threshold & Business Decisions | `06_threshold_and_business.ipynb` | Done |
| 7. Summary & Takeaways | `07_summary.ipynb` | Done |
| 8. Training Script | `src/models/train.py` | Done |
| 9. Scoring API | `app/main.py` (FastAPI) | Done |
| 10. Dashboard | `app/dashboard.py` (Streamlit) | Done |
| 11. Lead Simulator | `app/simulate.py` | Done |
| 12. Docker | `Dockerfile` | Done |

## Quick Start

```bash
# 1. Set up environment
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# 2. Run notebooks in order (01 → 06)
# Start with notebooks/01_data_fetch.ipynb

# 3. Train the model
python src/models/train.py

# 4. Start the scoring API
uvicorn app.main:app --port 8000

# 5. Start the dashboard (separate terminal)
streamlit run app/dashboard.py

# 6. Generate and score synthetic leads
python app/simulate.py -n 20 --score
```

## Tech Stack

- **Data**: Pandas, NumPy
- **ML**: scikit-learn, LightGBM, Optuna
- **Tracking**: MLflow
- **Serving**: FastAPI, Streamlit
- **Deployment**: Docker, GCP Cloud Run

## Business Questions

- Are we profitable overall at £55 per lead?
- Which lead segments (keyword, device, verification) are profitable vs. loss-making?
- Can we predict which leads will convert?
- Can we identify high-value leads early?
- Which keywords should we pause (zero conversions)?

## Tests

```bash
python -m pytest tests/ -v
```

13 tests covering API endpoints (health, scoring, validation, edge cases) and model artefact integrity.

## Docker

```bash
docker build -t leadsense .
docker run -p 8000:8000 -p 8501:8501 leadsense
```

Exposes the scoring API on port 8000 and Streamlit dashboard on port 8501.

## License

MIT
