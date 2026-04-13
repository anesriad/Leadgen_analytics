# Notebooks

Run them in order, 01 → 07. Each one writes the artefacts the next one needs.

| # | Notebook | Purpose |
|---|----------|---------|
| 01 | `01_data_fetch.ipynb` | Load `datasets/insurance_leadgen_data.csv` and take a first look |
| 02 | `02_clean_and_validate.ipynb` | Standardise columns, build target flags, validate with Pandera, save `data/leads_clean.parquet` |
| 03 | `03_eda_leads.ipynb` | Lead profitability — RPL by dimension, zero-sale keywords |
| 04 | `04_hypothesis_testing.ipynb` | Z-test, Kruskal-Wallis, A/B sample size |
| 05 | `05_modeling.ipynb` | Logistic baseline, LightGBM, Optuna tuning, save model bundle |
| 06 | `06_threshold_and_business.ipynb` | Threshold sweep, cumulative gains, CAC simulation |
| 07 | `07_summary.ipynb` | Findings and takeaways across the whole project |

### Key business constant

`COST_PER_LEAD = £55` — the actual cost we pay per lead. Used as the breakeven line in NB03 onwards.
