"""Check every lane's JSON against CONTRACTS.md. Run before every pull request:

    python scripts/check_contracts.py        (Windows: py scripts/check_contracts.py)

Missing output files are fine (that lane isn't done yet). Wrong keys, wrong types,
unknown site ids, or bad histogram lengths are errors. Exit code 1 if anything is wrong.
Standard library only, so it also runs in GitHub Actions without installs.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

errors, notes = [], []


def err(msg):
    errors.append(msg)


def load(path, required=False):
    if not os.path.exists(path):
        (err if required else notes.append)(f"{path}: missing" + ("" if required else " (ok, lane not done yet)"))
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        err(f"{path}: not valid JSON ({e})")
        return None


def is_num(v):
    return v is None or (isinstance(v, (int, float)) and not isinstance(v, bool))


def check_keys(path, sid, entry, spec):
    if not isinstance(entry, dict):
        err(f"{path}[{sid}]: should be an object")
        return
    for key, kind in spec.items():
        if key not in entry:
            err(f"{path}[{sid}]: missing key '{key}' (use null if unknown)")
            continue
        v = entry[key]
        if kind == "num" and not is_num(v):
            err(f"{path}[{sid}].{key}: should be a number or null, got {v!r}")
        elif kind == "score" and not (v is None or (is_num(v) and 0 <= v <= 1)):
            err(f"{path}[{sid}].{key}: should be between 0 and 1 or null, got {v!r}")
        elif isinstance(kind, int) and v is not None:
            if not (isinstance(v, list) and len(v) == kind and all(is_num(x) for x in v)):
                err(f"{path}[{sid}].{key}: should be a list of {kind} numbers or null")


def check_window(path, sid, w):
    if w is None:
        return
    if not (isinstance(w, dict) and {"start", "end", "days"} <= set(w)):
        err(f"{path}[{sid}].best_window: should be null or {{start, end, days}}")


sites = load("data/sites.json", required=True) or []
ids = {s["id"] for s in sites}
earth_ids = {s["id"] for s in sites if s.get("role") != "moon"}
for s in sites:
    for k in ("id", "name", "role"):
        if k not in s:
            err(f"data/sites.json: a site is missing '{k}'")
    if s.get("role") == "moon" and "dem" not in s:
        err(f"data/sites.json[{s.get('id')}]: Moon windows need 'dem'")
    if s.get("role") != "moon" and not (is_num(s.get("lat")) and is_num(s.get("lon"))):
        err(f"data/sites.json[{s.get('id')}]: Earth sites need numeric lat/lon")

# out/terrain.json (Member 1)
terrain = load("out/terrain.json")
if terrain:
    spec = {"slope_hist": 45, "rough_hist": 20, "slope_similarity": "score", "roughness_similarity": "score",
            "slope_p50_deg": "num", "slope_p90_deg": "num", "rough_p50_m": "num", "relief_m": "num",
            "valid_fraction": "score", "window_km": "num"}
    for sid, entry in terrain.items():
        if sid not in ids:
            err(f"out/terrain.json: unknown site id '{sid}'")
        else:
            check_keys("out/terrain.json", sid, entry, spec)

# out/sun.json (Member 2)
sun = load("out/sun.json")
if sun:
    spec = {"low_sun_hours": "num", "low_sun_fraction": "score", "median_daily_low_sun_min": "num",
            "band_speed_deg_per_hr": "num", "best_window": "any"}
    for sid, entry in sun.items():
        if sid == "_moon":
            continue
        if sid not in earth_ids:
            err(f"out/sun.json: unknown Earth site id '{sid}'")
        else:
            check_keys("out/sun.json", sid, entry, spec)
            check_window("out/sun.json", sid, entry.get("best_window"))

# out/temp.json (Member 2)
temp = load("out/temp.json")
if temp:
    for sid, entry in temp.items():
        if sid == "_moon":
            check_keys("out/temp.json", sid, entry, {"min_c": "num", "max_c": "num"})
        elif sid not in earth_ids:
            err(f"out/temp.json: unknown Earth site id '{sid}'")
        else:
            check_keys("out/temp.json", sid, entry, {"lst_min_c": "num", "lst_max_c": "num"})

# content/breaks.json (Member 4)
breaks = load("content/breaks.json")
if breaks:
    if not isinstance(breaks.get("_global"), list):
        err("content/breaks.json: '_global' should be a list of strings")
    for sid, entry in breaks.items():
        if sid == "_global":
            continue
        if sid not in earth_ids:
            err(f"content/breaks.json: unknown Earth site id '{sid}'")
            continue
        for k, kind in (("why", str), ("works", list), ("breaks", list), ("access", str)):
            if k not in entry:
                err(f"content/breaks.json[{sid}]: missing '{k}'")
            elif entry[k] is not None and not isinstance(entry[k], kind):
                err(f"content/breaks.json[{sid}].{k}: should be {kind.__name__}")

# web/mock_results.json and web/results.json (Member 3 / merge.py)
for path in ("web/mock_results.json", "web/results.json"):
    res = load(path, required=(path == "web/mock_results.json"))
    if not res:
        continue
    for k in ("sites", "moon", "cannot_reproduce", "weights"):
        if k not in res:
            err(f"{path}: missing top-level '{k}'")
    for s in res.get("sites", []):
        for k in ("id", "name", "lat", "lon", "role", "scores", "terrain", "best_window", "sun", "temp",
                  "why", "works", "breaks", "access"):
            if k not in s:
                err(f"{path}[{s.get('id')}]: missing '{k}'")
        sc = s.get("scores", {})
        for k in ("slope", "roughness", "low_sun", "overall"):
            if k not in sc:
                err(f"{path}[{s.get('id')}].scores: missing '{k}'")
    if path == "web/results.json" and res.get("mock"):
        err("web/results.json says mock: true - real results must not be mock data")

for n in notes:
    print("  note:", n)
if errors:
    print(f"\n{len(errors)} problem(s):")
    for e in errors:
        print("  x", e)
    sys.exit(1)
print("All contracts OK.")
