"""Join every lane's output into web/results.json (the file the app reads).

Inputs (all optional - a missing file just leaves nulls, so the app always loads):
  data/sites.json        everyone (frozen at H1)
  out/terrain.json       Member 1
  out/sun.json           Member 2
  out/temp.json          Member 2
  content/breaks.json    Member 4

Run from anywhere:  python merge.py      (Windows: py merge.py)
Output shape: see CONTRACTS.md -> web/results.json
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from constants import WEIGHTS  # noqa: E402

TERRAIN_KEYS = ("slope_p50_deg", "slope_p90_deg", "rough_p50_m", "relief_m", "slope_hist", "rough_hist")
SUN_KEYS = ("low_sun_hours", "low_sun_fraction", "median_daily_low_sun_min", "band_speed_deg_per_hr")
MOON_WINDOW_KEYS = ("slope_p50_deg", "slope_p90_deg", "rough_p50_m", "slope_similarity",
                    "roughness_similarity", "slope_hist", "rough_hist")


def load(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    print(f"  (missing {path} - using nulls)")
    return {}


def overall(scores):
    parts = [(WEIGHTS[k], v) for k, v in scores.items() if k in WEIGHTS and v is not None]
    if not parts:
        return None
    return round(sum(w * v for w, v in parts) / sum(w for w, _ in parts), 3)


def main():
    sites = load("data/sites.json")
    terrain = load("out/terrain.json")
    sun = load("out/sun.json")
    temp = load("out/temp.json")
    breaks = load("content/breaks.json")

    out_sites = []
    for s in sites:
        if s["role"] == "moon":
            continue
        t = terrain.get(s["id"]) or {}
        su = sun.get(s["id"]) or {}
        te = temp.get(s["id"]) or {}
        b = breaks.get(s["id"]) or {}
        scores = {
            "slope": t.get("slope_similarity"),
            "roughness": t.get("roughness_similarity"),
            "low_sun": su.get("low_sun_fraction"),
        }
        scores["overall"] = overall(scores)
        out_sites.append({
            "id": s["id"], "name": s["name"], "lat": s["lat"], "lon": s["lon"], "role": s["role"],
            "scores": scores,
            "terrain": {k: t.get(k) for k in TERRAIN_KEYS},
            "best_window": su.get("best_window"),
            "sun": {k: su.get(k) for k in SUN_KEYS},
            "temp": {"min_c": te.get("lst_min_c"), "max_c": te.get("lst_max_c")},
            "why": b.get("why"),
            "works": b.get("works") or [],
            "breaks": b.get("breaks") or [],
            "access": b.get("access"),
        })

    moon_windows = {}
    for s in sites:
        if s["role"] == "moon":
            v = terrain.get(s["id"])
            moon_windows[s["id"]] = {k: v.get(k) for k in MOON_WINDOW_KEYS} if v else None

    result = {
        "sites": out_sites,
        "moon": {
            "windows": moon_windows,
            "temp": temp.get("_moon") or {"min_c": None, "max_c": None},
            "sun": sun.get("_moon") or {"low_sun_fraction": None},
        },
        "cannot_reproduce": breaks.get("_global") or [],
        "weights": WEIGHTS,
    }
    os.makedirs("web", exist_ok=True)
    with open("web/results.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    scored = sum(1 for x in out_sites if x["scores"]["overall"] is not None)
    print(f"wrote web/results.json ({len(out_sites)} sites, {scored} with at least one score)")


if __name__ == "__main__":
    main()
