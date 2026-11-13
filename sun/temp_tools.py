"""Temperature helpers (Member 2).

Step 1 - make the points file to upload to NASA AppEEARS (https://appeears.earthdatacloud.nasa.gov):
    python sun/temp_tools.py points
  -> writes sun/appeears_points.csv. In AppEEARS: Extract -> Point Sample -> upload that CSV,
     product MOD11A2 (MODIS land surface temperature, 8-day, 1 km), layers LST_Day_1km and
     LST_Night_1km, dates 2025-01-01 to 2025-12-31. Submit tonight: requests are queued.

Step 2 - when AppEEARS emails you, download the results CSV into sun/ and run:
    python sun/temp_tools.py convert sun/<the-results-file>.csv
  -> writes out/temp.json with the yearly min (night) and max (day) per site in deg C.

Moon values: fill "_moon" in out/temp.json by hand from Diviner (LRO) for the two Moon windows,
with the source in "source". Leave null if not found; the app shows "n/a".
"""
import os as _os
import sys as _sys
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
_os.chdir(_ROOT)

import csv
import json
import os
import sys


def make_points():
    sites = [s for s in json.load(open("data/sites.json")) if s["role"] != "moon"]
    with open("sun/appeears_points.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ID", "Category", "Latitude", "Longitude"])
        for s in sites:
            w.writerow([s["id"], s["role"], s["lat"], s["lon"]])
    print(f"wrote sun/appeears_points.csv ({len(sites)} points)")


def to_celsius(v):
    v = float(v)
    if v <= 0:
        return None          # fill value / no data
    if v > 1000:             # raw scaled integer (scale 0.02)
        v *= 0.02
    return v - 273.15        # Kelvin -> Celsius


def convert(path):
    rows = list(csv.DictReader(open(path, newline="")))
    if not rows:
        raise SystemExit("empty CSV")
    cols = rows[0].keys()
    day = next(c for c in cols if "LST_Day" in c and "QC" not in c)
    night = next(c for c in cols if "LST_Night" in c and "QC" not in c)
    idcol = "ID" if "ID" in cols else next(iter(cols))

    acc = {}
    for r in rows:
        a = acc.setdefault(r[idcol], {"max": [], "min": []})
        d, n = to_celsius(r[day] or 0), to_celsius(r[night] or 0)
        if d is not None:
            a["max"].append(d)
        if n is not None:
            a["min"].append(n)

    out = json.load(open("out/temp.json")) if os.path.exists("out/temp.json") else {}
    for sid, a in acc.items():
        out[sid] = {"lst_min_c": round(min(a["min"]), 1) if a["min"] else None,
                    "lst_max_c": round(max(a["max"]), 1) if a["max"] else None}
    out.setdefault("_moon", {"min_c": None, "max_c": None, "source": "Diviner (LRO) - fill in"})
    json.dump(out, open("out/temp.json", "w"), indent=1)
    print(f"wrote out/temp.json ({len(acc)} sites)")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "points":
        make_points()
    elif len(sys.argv) >= 3 and sys.argv[1] == "convert":
        convert(sys.argv[2])
    else:
        print(__doc__)
