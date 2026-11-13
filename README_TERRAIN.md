"""Join every lane's output into web/results.json (the file the app reads).

Inputs (all optional - a missing file just leaves nulls):
data/sites.json everyone
out/terrain.json Member 1
out/sun.json Member 2
out/temp.json Member 2
content/breaks.json Member 4

Run any time: python merge.py
"""
import json
import os

from constants import WEIGHTS

def load(path):
if os.path.exists(path):
with open(path) as f:
return json.load(f)
print(f" (missing {path} - using nulls)")
return {}

def overall(scores):
parts = [(WEIGHTS[k], v) for k, v in scores.items() if k in WEIGHTS and v is not None]
if not parts:
return None
return round(sum(w \* v for w, v in parts) / sum(w for w, \_ in parts), 3)

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
        t, su, te, b = (terrain.get(s["id"]) or {}, sun.get(s["id"]) or {},
                        temp.get(s["id"]) or {}, breaks.get(s["id"]) or {})
        scores = {
            "slope": t.get("slope_similarity"),
            "roughness": t.get("roughness_similarity"),
            "low_sun": su.get("low_sun_fraction"),
        }
        scores["overall"] = overall(scores)
        out_sites.append({
            "id": s["id"], "name": s["name"], "lat": s["lat"], "lon": s["lon"], "role": s["role"],
            "scores": scores,
            "terrain": {k: t.get(k) for k in ("slope_p50_deg", "slope_p90_deg", "rough_p50_m",
                                              "relief_m", "slope_hist", "rough_hist")},
            "best_window": su.get("best_window"),
            "temp": {"min_c": te.get("lst_min_c"), "max_c": te.get("lst_max_c")},
            "why": b.get("why"), "works": b.get("works", []),
            "breaks": b.get("breaks", []), "access": b.get("access"),
        })

    moons = {s["id"]: terrain.get(s["id"]) for s in sites if s["role"] == "moon"}
    result = {
        "sites": out_sites,
        "moon": {
            "windows": {k: ({kk: v.get(kk) for kk in ("slope_p50_deg", "slope_p90_deg", "rough_p50_m",
                                                      "slope_similarity", "roughness_similarity",
                                                      "slope_hist", "rough_hist")} if v else None)
                        for k, v in moons.items()},
            "temp": temp.get("_moon"),
        },
        "cannot_reproduce": breaks.get("_global", []),
        "weights": WEIGHTS,
    }
    os.makedirs("web", exist_ok=True)
    with open("web/results.json", "w") as f:
        json.dump(result, f, indent=1)
    print(f"wrote web/results.json ({len(out_sites)} sites)")

if **name** == "**main**":
main()
