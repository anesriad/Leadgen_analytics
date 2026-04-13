"""Generate synthetic leads and optionally score them via the API."""

import argparse
import json
import random
import sys
from pathlib import Path

import pandas as pd
import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STAGING = PROJECT_ROOT / "data" / "staging"
API_URL = "http://localhost:8000/score"


def _load_distributions() -> dict:
    """Sample value distributions from real staging data."""
    df = pd.read_parquet(STAGING / "leads_clean.parquet")
    return {
        "gender": df["gender"].value_counts(normalize=True).to_dict(),
        "smoker": df["smoker"].value_counts(normalize=True).to_dict(),
        "current_insurance": df["current_insurance"].value_counts(normalize=True).to_dict(),
        "device_type": df["device_type"].value_counts(normalize=True).to_dict(),
        "match_type": df["match_type"].value_counts(normalize=True).to_dict(),
        "cover_for": df["cover_for"].value_counts(normalize=True).to_dict(),
        "verification_status": df["verification_status"].value_counts(normalize=True).to_dict(),
        "keyword_group": df["keyword_group"].value_counts(normalize=True).to_dict(),
        "pc_area": df["pc_area"].value_counts(normalize=True).to_dict(),
        "age_mean": float(df["age"].mean()),
        "age_std": float(df["age"].std()),
    }


def _weighted_choice(dist: dict) -> str:
    return random.choices(list(dist.keys()), weights=list(dist.values()), k=1)[0]


def generate_lead(dists: dict) -> dict:
    age = max(18, min(120, int(random.gauss(dists["age_mean"], dists["age_std"]))))
    return {
        "age": age,
        "gender": _weighted_choice(dists["gender"]),
        "smoker": _weighted_choice(dists["smoker"]),
        "current_insurance": _weighted_choice(dists["current_insurance"]),
        "device_type": _weighted_choice(dists["device_type"]),
        "match_type": _weighted_choice(dists["match_type"]),
        "cover_for": _weighted_choice(dists["cover_for"]),
        "verification_status": _weighted_choice(dists["verification_status"]),
        "keyword_group": _weighted_choice(dists["keyword_group"]),
        "pc_area": _weighted_choice(dists["pc_area"]),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic leads")
    parser.add_argument("-n", type=int, default=10, help="Number of leads (default: 10)")
    parser.add_argument("--score", action="store_true", help="POST each lead to the scoring API")
    parser.add_argument("--json", action="store_true", help="Print as JSON array")
    args = parser.parse_args()

    dists = _load_distributions()
    leads = [generate_lead(dists) for _ in range(args.n)]

    if args.score:
        for i, lead in enumerate(leads, 1):
            try:
                resp = requests.post(API_URL, json=lead, timeout=5)
                resp.raise_for_status()
                result = resp.json()
                print(f"[{i}/{args.n}] prob={result['conversion_probability']:.3f}  "
                      f"tier={result['risk_tier']:6s}  age={lead['age']}  "
                      f"kw={lead['keyword_group']}")
            except requests.ConnectionError:
                print("ERROR: API not reachable. Start it first.", file=sys.stderr)
                sys.exit(1)
    elif args.json:
        print(json.dumps(leads, indent=2))
    else:
        df = pd.DataFrame(leads)
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()
