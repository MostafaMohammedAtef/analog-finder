"""Validate reference analog locations against generated scores."""

from pathlib import Path
import sys

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main(target_name):
    scores = pd.read_csv(ROOT / "out" / f"scores_{target_name}.csv")
    analogs = pd.read_csv(ROOT / "data" / "known_analogs.csv")
    for _, analog in analogs.iterrows():
        distances = (scores["lat"] - analog["lat"]) ** 2 + (
            (scores["lon"] - analog["lon"]) * np.cos(np.radians(analog["lat"]))
        ) ** 2
        nearest = scores.loc[distances.idxmin()]
        percentile = (scores["score"] <= nearest["score"]).mean() * 100
        print(
            f"{analog['name']}: nearest={nearest['cell_id']}, "
            f"score={nearest['score']:.3f}, percentile={percentile:.1f}"
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python member3_scoring/validate.py <target_name>")
    main(sys.argv[1])
