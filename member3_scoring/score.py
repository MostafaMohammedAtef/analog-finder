"""Score Earth grid cells against a planetary target."""

from pathlib import Path
import json
import sys

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["slope_deg", "temp_range_k", "ndvi", "precip_mm_yr", "dust_idx"]
DEFAULT_WEIGHTS = {feature: 1.0 for feature in FEATURES}
DEFAULT_SCALES = {
    "slope_deg": 10.0,
    "temp_range_k": 20.0,
    "ndvi": 0.2,
    "precip_mm_yr": 500.0,
    "dust_idx": 0.3,
}


def score(earth_df, target_dict, weights=None, scales=None):
    """Return scores and per-feature similarities for every Earth cell."""
    weights = weights or DEFAULT_WEIGHTS
    scales = scales or DEFAULT_SCALES
    similarities = {
        f"sim_{feature}": np.exp(
            -np.abs(earth_df[feature] - target_dict[feature]) / scales[feature]
        )
        for feature in FEATURES
    }
    result = earth_df[["cell_id", "lat", "lon"]].copy()
    result = pd.concat([result, pd.DataFrame(similarities, index=earth_df.index)], axis=1)
    weight_values = np.array([weights[feature] for feature in FEATURES], dtype=float)
    sim_values = result[[f"sim_{feature}" for feature in FEATURES]].to_numpy()
    result["score"] = (sim_values * weight_values).sum(axis=1) / weight_values.sum()
    columns = ["cell_id", "lat", "lon", "score"] + [
        f"sim_{feature}" for feature in FEATURES
    ]
    return result[columns].sort_values("score", ascending=False).reset_index(drop=True)


def main(target_name):
    with (ROOT / "data" / "targets.json").open(encoding="utf-8") as file:
        targets = json.load(file)
    if target_name not in targets:
        raise SystemExit(f"Unknown target {target_name!r}; choose from {', '.join(targets)}")
    earth = pd.read_csv(ROOT / "data" / "earth_grid.csv")
    output = score(earth, targets[target_name], DEFAULT_WEIGHTS, DEFAULT_SCALES)
    output_path = ROOT / "out" / f"scores_{target_name}.csv"
    output_path.parent.mkdir(exist_ok=True)
    output.to_csv(output_path, index=False)
    print(f"Wrote {len(output)} scores to {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python member3_scoring/score.py <target_name>")
    main(sys.argv[1])
