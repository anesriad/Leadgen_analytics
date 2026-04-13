"""Train the lead scoring model and save artefacts for serving."""

import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score
import lightgbm as lgb

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
STAGING = PROJECT_ROOT / "data" / "staging"
ARTEFACTS = PROJECT_ROOT / "app" / "artefacts"
ARTEFACTS.mkdir(parents=True, exist_ok=True)

NUMERIC_FEATS = ["age"]
CAT_FEATS = [
    "gender", "smoker", "current_insurance", "device_type",
    "match_type", "cover_for", "verification_status",
    "keyword_group", "pc_area",
]
TARGET = "converted"

# --- Load & encode ---
df = pd.read_parquet(STAGING / "leads_clean.parquet")
X = df[NUMERIC_FEATS + CAT_FEATS].copy()
y = df[TARGET]

encoders = {}
for col in CAT_FEATS:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le

# --- Train ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y,
)

neg, pos = (y_train == 0).sum(), (y_train == 1).sum()
model = lgb.LGBMClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    num_leaves=31,
    scale_pos_weight=neg / pos,
    random_state=42,
    verbosity=-1,
)
model.fit(X_train, y_train)

probs = model.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, probs)
print(f"Test ROC-AUC: {auc:.4f}")

# --- Save ---
joblib.dump(model, ARTEFACTS / "model.joblib")
joblib.dump(encoders, ARTEFACTS / "encoders.joblib")
joblib.dump(NUMERIC_FEATS + CAT_FEATS, ARTEFACTS / "feature_names.joblib")

print(f"Saved to {ARTEFACTS}/")
