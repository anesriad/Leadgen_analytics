# LeadSense — Lead Acquisition Profitability

A notebook-driven analytics study of an insurance lead generation business, paired with a Streamlit dashboard for interactive exploration.

The project answers a single, very concrete commercial question:

> **At £55 per lead, which segments are profitable, which are losing money, and can a model help us prioritise which leads to chase first?**

## Quick Start

Get the project running on your machine in five steps. You don't need any account, key, or external service — everything runs locally on the dataset shipped in this repo.

### 1. Clone the repo

```bash
git clone https://github.com/anesriad/Leadgen_analytics.git
cd Leadgen_analytics
```

### 2. Create a virtual environment

A virtual environment keeps the project's Python packages isolated from the rest of your system. Pick whichever command matches your OS:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

You should see `(.venv)` appear at the start of your prompt — that means the environment is active.

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

This installs pandas, scikit-learn, LightGBM, Pandera, Streamlit and everything else the notebooks and dashboard need. It takes a couple of minutes the first time.

### 4. Run the notebooks in order

```bash
jupyter lab notebooks/
```

Open the notebooks one at a time and run them top to bottom in this order:

1. `01_data_fetch.ipynb` — load and describe the data
2. `02_clean_and_validate.ipynb` — clean, validate, and save `data/leads_clean.parquet`
3. `03_eda_leads.ipynb` — exploratory analysis
4. `04_hypothesis_testing.ipynb` — statistical tests
5. `05_modeling.ipynb` — train models and save `data/lead_model.joblib`
6. `06_threshold_and_business.ipynb` — threshold tuning and business simulation
7. `07_summary.ipynb` — final takeaways

You only need to run NB02 and NB05 for the dashboard to work — the others are for reading and following along, but every notebook is self-contained and can be re-run any time.

### 5. Launch the dashboard

In a new terminal (with the virtual environment still activated):

```bash
streamlit run app/dashboard.py
```

Streamlit will open a browser tab at `http://localhost:8501`. The dashboard has three pages — **Overview**, **Dimensional Analysis**, and **Lead Scorer** — and reads directly from the parquet and model files you just generated.

That's it. No accounts, no API keys, no cloud setup. If you can run Python and Jupyter on your machine, you can run the whole project.

## Why this project

Most lead-gen businesses live and die by a handful of numbers — RPL (revenue per lead), CAC (cost per acquisition), conversion rate, ROAS — and most of the value comes from understanding *which segments* drive those numbers up or down. This project takes a real-shaped insurance lead dataset and works through that question end to end, from raw CSV to interactive dashboard, using only what's necessary at each step.

It's deliberately scoped as **a thinking project, not a system project**. There is no FastAPI service, no Docker image, no CI pipeline, no cloud deployment. Every artefact is a notebook or a small Streamlit app. The point is to be clear, reproducible, and easy for someone else to read and learn from.

## The dataset

`datasets/insurance_leadgen_data.csv` is a prepared version of an internal insurance lead-generation dataset. Before the file was committed to this repo it was tidied up so it could be shared safely:

- **Lead IDs were anonymised** — replaced with random 8-digit numbers so individual records can't be traced back.
- **~5% of unverified leads were dropped** — the weakest part of the funnel was thinned out, mostly to shrink the file and remove the lowest-signal rows.
- **~10% of synthetic rows were added** — to balance the sample and round it out.
- **Column names were converted to snake_case** so they're easy to use in code.

The CSV is the project's source of truth. There is no upstream raw file or fetch step — `01_data_fetch.ipynb` simply loads the CSV and describes it.

### What's in the data

| Column | What it is |
|---|---|
| `lead_id` | Anonymised 8-digit lead identifier |
| `lead_status` | Funnel state — `Contacted`, `No Contact`, `Quoted`, `Sold`, `Invalid` |
| `premium` | Premium amount if the lead was sold (£0 otherwise) |
| `age`, `gender`, `smoker` | Demographics |
| `current_insurance` | Whether the lead already has insurance |
| `device_type` | `Desktop`, `Smartphone`, `Tablet` |
| `keyword`, `match_type` | The search keyword that brought the lead in and how it matched the ad |
| `postcode` | UK postcode (used to derive `pc_area` in NB02) |
| `cover_for` | Who the cover is for — `Self`, `Self + Partner`, etc. |
| `verification_status` | Whether the lead was verified |

## Project structure

```
leadgen project ML/
├── README.md                        # this file
├── requirements.txt
├── datasets/
│   └── insurance_leadgen_data.csv   # the prepared source CSV
├── data/
│   ├── leads_clean.parquet          # generated by NB02
│   └── lead_model.joblib            # generated by NB05
├── notebooks/
│   ├── 01_data_fetch.ipynb
│   ├── 02_clean_and_validate.ipynb
│   ├── 03_eda_leads.ipynb
│   ├── 04_hypothesis_testing.ipynb
│   ├── 05_modeling.ipynb
│   ├── 06_threshold_and_business.ipynb
│   ├── 07_summary.ipynb
│   └── README.md
├── app/
│   └── dashboard.py                 # Streamlit dashboard
└── Project Context/
    └── project1_marketing_ml_summary.md
```

The two files in `data/` are generated by running the notebooks (see [Quick Start](#quick-start)). They're git-ignored, so a fresh clone won't have them — running NB02 and NB05 will produce them. The dashboard reads both files; if you skip NB05 the first two dashboard pages still work, only the Lead Scorer page needs the model.

## What each notebook does

### 01 — Load the lead data
A thin entry-point notebook. Reads the CSV, shows the columns, breaks down `lead_status` and `verification_status`, and explains what was already done to prepare the file before it landed in the repo.

### 02 — Clean & validate
Standardises text columns, fills missing `verification_status`, derives a postcode area, groups keywords into intent-based buckets (Brand: Bupa / Generic Health / Comparison / Price intent / etc.), creates the `converted`, `is_invalid` and `high_value` target flags, and adds age bands and a synthetic `created_date`. Then it validates the result with **Pandera** — a typed schema check that fails loudly if any column is the wrong type, has values outside the expected range, or contains an unexpected category. The cleaned DataFrame is saved as `data/leads_clean.parquet`.

### 03 — EDA: lead profitability
The headline analyst story. Computes the commercial summary (total leads, conversions, RPL, net per lead, ROI), shows the funnel, then breaks down RPL by verification, device, keyword group, current insurance, smoker status, and `cover_for`. Identifies zero-sale keywords — keywords with 15+ leads that converted *nobody* — which represent pure waste at £55/lead.

### 04 — Hypothesis testing
Three statistical tests aimed at validating what NB03 found:
- **Z-test for two proportions** — does verification status really shift conversion rate, or is the gap noise?
- **Kruskal-Wallis** — do keyword groups really have different RPL distributions?
- **Sample size calculation** — if we wanted to A/B test a change to the funnel, how many leads per arm would we need?

Each test has a short plain-English intro and links to a visual explainer for viewers who want a refresher.

### 05 — Modeling
Predict `converted = 1`. Three steps: a logistic regression baseline, a default LightGBM, and an Optuna-tuned LightGBM. Documents the leakage and multicollinearity reasoning behind the feature list. All three models land at roughly **0.58 ROC-AUC** — covered honestly in the conclusion. The tuned model is saved as a single `data/lead_model.joblib` bundle (model + label encoders + feature order) for the dashboard to load.

### 06 — Threshold tuning & business decisions
Self-contained re-train, then a threshold sweep, a cumulative gains chart, and a CAC simulation. Shows that even with a weak AUC, **ranking** leads by score still cuts effective CAC from ~£1,128 to ~£850 by letting the sales team prioritise the top half of the pipeline.

### 07 — Summary
The whole-project recap: what we found, what's actionable, and what a viewer should take away. Designed to read on its own.

## On the modelling result

The model tops out at about **0.58 ROC-AUC** across all three approaches — logistic regression, default LightGBM, and Optuna-tuned LightGBM. That's only slightly better than a coin flip, and it's the most interesting result in the project, so it's worth being upfront about why.

The features available in this dataset describe **who the lead is** and **how they arrived** (age, gender, device, keyword group, postcode area, verification status). They say very little about the things that actually drive conversion — budget, urgency, the quality of the call-back, the lead's specific health situation, what they were quoted. With a feature ceiling like that, no amount of hyperparameter tuning is going to break through. LightGBM and logistic regression both end up squeezing the same small amount of signal out of the same set of columns.

To meaningfully push past 0.58 the project would need **behavioural features** that simply don't exist in this dataset — time-on-page, quote interactions, call duration, number of touches across the funnel.

**The takeaway is the lesson, not the AUC.** Most ML tutorials quietly pick datasets where a default XGBoost hits 0.95 and the magic looks easy. Real projects don't work that way — the most common failure mode is exactly this one, where you've extracted everything the data has to give and it isn't enough. Recognising that early is what saves a project from a week of pointless tuning, and points you at the real next move: getting better data, not a better model.

And then NB06 flips the framing: a 0.58 AUC ranker is **still commercially useful**. Ranking leads by score and calling the top half first cuts effective CAC by roughly 25%. AUC is a model metric; CAC is a business metric. The whole point of doing this end to end is learning to optimise the second one.

## Tech stack

| Layer | Tools |
|---|---|
| Data manipulation | pandas, numpy, pyarrow |
| Validation | Pandera |
| Statistics | scipy, statsmodels |
| Machine learning | scikit-learn, LightGBM, Optuna |
| Visualisation | matplotlib, seaborn, plotly |
| Dashboard | Streamlit |
| Notebooks | Jupyter |

Everything runs locally with no external services.

## License

MIT
