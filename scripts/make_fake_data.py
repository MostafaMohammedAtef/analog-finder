"""Generate deterministic, plausible demo data for Analog Finder."""

from pathlib import Path
import json

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

KNOWN_ANALOGS = [
    ("Atacama", -23.7, -69.2),
    ("Mojave", 35.0, -117.0),
    ("Haughton crater", 75.4, -89.7),
    ("Antarctica Dry Valleys", -77.5, 161.5),
    ("Iceland", 65.0, -18.8),
    ("Gilf Kebir Egypt", 24.7, 25.7),
    ("Bahariya Egypt", 28.3, 28.9),
]


def main():
    rng = np.random.default_rng(42)
    n_cells = 2000
    earth = pd.DataFrame(
        {
            "cell_id": [f"cell_{i:04d}" for i in range(n_cells)],
            "lat": rng.uniform(-90, 90, n_cells),
            "lon": rng.uniform(-180, 180, n_cells),
            "slope_deg": rng.uniform(0, 30, n_cells),
            "elev_m": rng.uniform(-400, 5000, n_cells),
            "temp_range_k": rng.uniform(5, 60, n_cells),
            "ndvi": rng.uniform(0, 0.8, n_cells),
            "precip_mm_yr": rng.uniform(0, 3000, n_cells),
            "dust_idx": rng.uniform(0, 1, n_cells),
        }
    )

    # Add one close, desert-like cell for each reference analog.
    desert_values = {
        "slope_deg": 8.0,
        "elev_m": 900.0,
        "temp_range_k": 45.0,
        "ndvi": 0.02,
        "precip_mm_yr": 8.0,
        "dust_idx": 0.88,
    }
    for index, (_, lat, lon) in enumerate(KNOWN_ANALOGS):
        row = {"cell_id": f"analog_{index + 1:02d}", "lat": lat, "lon": lon}
        row.update(desert_values)
        row["lat"] += rng.uniform(-0.15, 0.15)
        row["lon"] += rng.uniform(-0.15, 0.15)
        earth = pd.concat([earth, pd.DataFrame([row])], ignore_index=True)

    DATA_DIR.mkdir(exist_ok=True)
    earth.to_csv(DATA_DIR / "earth_grid.csv", index=False)
    with (DATA_DIR / "targets.json").open("w", encoding="utf-8") as file:
        json.dump(
            {
                "jezero": {
                    "slope_deg": 8.0,
                    "temp_range_k": 45.0,
                    "ndvi": 0.0,
                    "precip_mm_yr": 10.0,
                    "dust_idx": 0.85,
                },
                "shackleton_rim": {
                    "slope_deg": 12.0,
                    "temp_range_k": 20.0,
                    "ndvi": 0.0,
                    "precip_mm_yr": 0.0,
                    "dust_idx": 0.65,
                },
            },
            file,
            indent=2,
        )
    pd.DataFrame(KNOWN_ANALOGS, columns=["name", "lat", "lon"]).to_csv(
        DATA_DIR / "known_analogs.csv", index=False
    )
    print(f"Generated {len(earth)} Earth grid cells and two targets.")


if __name__ == "__main__":
    main()
