# Data

All project data lives here, organized into three layers.

## Layers

### `raw/`
Original data as extracted — never modified.
- `leads/` — anonymized insurance lead CSV (~7.5K leads, random IDs, simplified columns)
- `spend/` — synthetic marketing spend data (weekly × keyword_group × device × match)

### `staging/`
Cleaned and standardized data. Text normalized, keyword groups assigned, target flags created, dates added.

### `mart/`
Final analytics-ready table. Leads aggregated weekly and joined to spend, with KPIs (RPL, CAC, ROAS) pre-calculated.

## Important
- Raw files are read-only. All transformations happen in staging/mart.
- Large files are gitignored. Re-generate them by running the notebooks.
