"""Write web/mock_results.json: FAKE numbers in the exact results.json shape (see CONTRACTS.md).
The app uses it until merge.py writes the real web/results.json.

Run from the repo root:  python web/make_mock.py
"""
import json
import os
import random

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
random.seed(42)

sites = json.load(open("data/sites.json"))
breaks = json.load(open("content/breaks.json")) if os.path.exists("content/breaks.json") else {}


def hist(n):
    v = [random.random() ** 3 for _ in range(n)]
    t = sum(v)
    return [round(x / t, 3) for x in v]


out_sites = []
for s in sites:
    if s["role"] == "moon":
        continue
    polar = abs(s["lat"]) > 60
    scores = {"slope": round(random.uniform(0.2, 0.6), 3),
              "roughness": round(random.uniform(0.2, 0.6), 3),
              "low_sun": round(random.uniform(0.12, 0.22) if polar else random.uniform(0.06, 0.08), 3)}
    scores["overall"] = round(sum(scores.values()) / 3, 3)
    b = breaks.get(s["id"], {})
    out_sites.append({
        "id": s["id"], "name": s["name"], "lat": s["lat"], "lon": s["lon"], "role": s["role"],
        "scores": scores,
        "terrain": {"slope_p50_deg": round(random.uniform(1, 8), 1), "slope_p90_deg": round(random.uniform(5, 25), 1),
                    "rough_p50_m": round(random.uniform(0.5, 6), 1), "relief_m": round(random.uniform(50, 900)),
                    "slope_hist": hist(45), "rough_hist": hist(20)},
        "best_window": {"start": "08-20", "end": "10-15", "days": 56} if polar else None,
        "sun": {"low_sun_hours": 700 if polar else 310, "low_sun_fraction": scores["low_sun"],
                "median_daily_low_sun_min": 240 if polar else 48,
                "band_speed_deg_per_hr": round(random.uniform(1.2, 3.8), 2) if polar else round(random.uniform(11, 13.3), 2)},
        "temp": {"min_c": round(random.uniform(-45, 5)), "max_c": round(random.uniform(10, 65))},
        "why": b.get("why"), "works": ["(mock) Similar slope distribution"], "breaks": ["(mock) Atmosphere scatters light"],
        "access": b.get("access"),
    })

mock = {
    "mock": True,
    "sites": out_sites,
    "moon": {"windows": {}, "temp": {"min_c": None, "max_c": None}, "sun": {"low_sun_fraction": 1.0}},
    "cannot_reproduce": breaks.get("_global", ["1/6 gravity", "Vacuum", "Radiation"]),
    "weights": {"slope": 1.0, "roughness": 1.0, "low_sun": 1.0},
}
json.dump(mock, open("web/mock_results.json", "w"), indent=1)
print(f"wrote web/mock_results.json ({len(out_sites)} sites, FAKE numbers)")
