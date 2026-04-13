# Source Code

Python modules for the LeadSense pipeline.

## What's here

### `models/train.py`
Training script — loads staging data, label-encodes categoricals, trains LightGBM with class weighting, and saves three artefacts to `app/artefacts/`:
- `model.joblib` — trained classifier
- `encoders.joblib` — fitted LabelEncoders per categorical column
- `feature_names.joblib` — ordered feature list

```bash
python src/models/train.py
```

### `data/`, `features/`, `pipelines/`, `monitoring/`
Placeholder modules — reserved for future refactoring if notebooks are promoted to production scripts.
