"""Join every lane's output into web/results.json (the file the app reads).

Inputs (all optional - a missing file just leaves nulls):
  data/sites.json        everyone
  out/terrain.json       Member 1  (Moon and Mars terrain scores)
  out/sun.json           Member 2
  out/temp.json          Member 2
  content/breaks.json    Member 4  (also found at ../content/ or "../Member 4/")

Run any time (from the terrain folder):
  python merge.py                         # writes web/results.json
  python merge.py --out ../results.json   # write it next to the app's index.html instead

Output: per site, "scores" = Moon (unchanged), "scores_mars" = Mars terrain (slope, roughness,
overall). Mars has no low-sun score: Mars gets ordinary sunrises and sunsets.
"""
import argparse
import json
import os

from constants import WEIGHTS


def load(*paths):
    for path in paths:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    print(f"  (missing {paths[0]} - using nulls)")
    return {}


def overall(scores):
    parts = [(WEIGHTS[k], v) for k, v in scores.items() if k in WEIGHTS and v is not None]
    if not parts:
        return None
    return round(sum(w * v for w, v in parts) / sum(w for w, _ in parts), 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="web/results.json")
    args = ap.parse_args()

    sites = load("data/sites.json")
    terrain = load("out/terrain.json")
    sun = load("out/sun.json", "../out/sun.json")
    temp = load("out/temp.json", "../out/temp.json")
    breaks = load("content/breaks.json", "../content/breaks.json", "../Member 4/breaks.json")

    out_sites = []
    for s in sites:
        if s["role"] in ("moon", "mars"):
            continue
        t, su, te, b = (terrain.get(s["id"]) or {}, sun.get(s["id"]) or {},
                        temp.get(s["id"]) or {}, breaks.get(s["id"]) or {})
        scores = {
            "slope": t.get("slope_similarity"),
            "roughness": t.get("roughness_similarity"),
            "low_sun": su.get("low_sun_fraction"),
        }
        scores["overall"] = overall(scores)
        scores_mars = {
            "slope": t.get("mars_slope_similarity"),
            "roughness": t.get("mars_roughness_similarity"),
        }
        scores_mars["overall"] = overall(scores_mars)
        out_sites.append({
            "id": s["id"], "name": s["name"], "lat": s["lat"], "lon": s["lon"], "role": s["role"],
            "scores": scores,
            "scores_mars": scores_mars,
            "terrain": {k: t.get(k) for k in ("slope_p50_deg", "slope_p90_deg", "rough_p50_m",
                                              "relief_m", "slope_hist", "rough_hist")},
            "best_window": su.get("best_window"),
            "temp": {"min_c": te.get("lst_min_c"), "max_c": te.get("lst_max_c")},
            "why": b.get("why"), "works": b.get("works", []),
            "breaks": b.get("breaks", []), "access": b.get("access"),
        })

    win_keys = ("slope_p50_deg", "slope_p90_deg", "rough_p50_m", "slope_similarity",
                "roughness_similarity", "mars_slope_similarity", "mars_roughness_similarity",
                "slope_hist", "rough_hist")

    def windows(role):
        return {s["id"]: ({kk: terrain[s["id"]].get(kk) for kk in win_keys}
                          if terrain.get(s["id"]) else None)
                for s in sites if s["role"] == role}

    result = {
        "sites": out_sites,
        "moon": {
            "windows": windows("moon"),
            "temp": temp.get("_moon"),
        },
        "mars": {
            "windows": windows("mars"),
        },
        "cannot_reproduce": breaks.get("_global", []),
        "weights": WEIGHTS,
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    n_mars = sum(1 for x in out_sites if x["scores_mars"]["overall"] is not None)
    print(f"wrote {args.out} ({len(out_sites)} sites, {n_mars} with Mars scores)")


if __name__ == "__main__":
    main()
