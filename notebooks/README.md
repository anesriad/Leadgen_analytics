# Notebooks

Jupyter notebooks for data exploration and experimentation. Run them in order (00 → 04+).

| # | Notebook | Purpose | Status |
|---|----------|---------|--------|
| 00 | `00_dataset_prep.ipynb` | Anonymize original data (5% cut, new IDs, rename cols) — run once | Done |
| 01 | `01_data_fetch.ipynb` | Load clean CSV, generate synthetic spend | Done |
| 02 | `02_clean_and_validate.ipynb` | Clean → staging, build mart table with KPIs | Done |
| 03 | `03_eda_leads.ipynb` | Lead profitability — RPL by dimension, zero-sale keywords | Done |
| 04 | `04_hypothesis_testing.ipynb` | Statistical tests + A/B sample size example | Done |
| 05 | `05_modeling.ipynb` | ML — baseline, LightGBM, Optuna tuning, MLflow | Done |
| 06 | `06_threshold_and_business.ipynb` | Threshold tuning, lift analysis, business sim | Done |
| 07 | `07_summary.ipynb` | Key findings & takeaways across all notebooks | Done |

### Key business constant

`COST_PER_LEAD = £55` — actual cost per lead from the account. Used throughout notebooks 03+ as the breakeven threshold for RPL (Revenue Per Lead) analysis.
