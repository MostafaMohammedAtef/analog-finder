"""Sun lane (Member 2): how much lunar-south-pole-like light each Earth site gets.

At the lunar south pole the Sun stays roughly 1-2 degrees above the horizon and
moves very slowly. For each Earth site we compute, over one year (10-minute steps,
flat horizon):

  low_sun_hours            hours with sun elevation between 0 and 5 degrees
  low_sun_fraction         those hours / all daylight hours   (Moon ~ 1.0)
  median_daily_low_sun_min typical minutes of low sun on days that have any
  band_speed_deg_per_hr    how fast the Sun moves through the band (Moon: almost 0)
  best_window              longest run of days with >= 2 h of low sun (null if none)

Writes out/sun.json.   Usage:  python sun/sun.py   [--year 2027]
Needs: pip install pvlib pandas
"""
import os as _os
import sys as _sys
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
_os.chdir(_ROOT)  # all paths below are relative to the repo root

import argparse
import json
import os

import numpy as np
import pandas as pd
import pvlib

from constants import LOW_SUN_MAX_DEG, LOW_SUN_MIN_DEG

STEP_MIN = 10
WINDOW_MIN_PER_DAY = 120   # a "good test day" has at least 2 h of low sun


def longest_run(good_days, dates):
    """Longest run of consecutive good days, allowing wrap from December to January."""
    n = len(good_days)
    if not good_days.any():
        return None
    if good_days.all():
        return {"start": dates[0].strftime("%m-%d"), "end": dates[-1].strftime("%m-%d"), "days": n}
    doubled = np.concatenate([good_days, good_days])
    best_len, best_start, run, start = 0, 0, 0, 0
    for i, g in enumerate(doubled):
        if g:
            if run == 0:
                start = i
            run += 1
            if run > best_len and run <= n:
                best_len, best_start = run, start
        else:
            run = 0
    s, e = dates[best_start % n], dates[(best_start + best_len - 1) % n]
    return {"start": s.strftime("%m-%d"), "end": e.strftime("%m-%d"), "days": int(best_len)}


def site_sun(lat, lon, year):
    times = pd.date_range(f"{year}-01-01", f"{year + 1}-01-01", freq=f"{STEP_MIN}min",
                          tz="UTC", inclusive="left")
    el = pvlib.solarposition.get_solarposition(times, lat, lon)["apparent_elevation"].to_numpy()
    step_h = STEP_MIN / 60
    above = el > 0
    band = (el > LOW_SUN_MIN_DEG) & (el < LOW_SUN_MAX_DEG)

    # Daily minutes in the band, by local solar day (UTC shifted by longitude)
    local_day = (times + pd.to_timedelta(lon / 15, unit="h")).normalize()
    daily = pd.Series(band.astype(int) * STEP_MIN, index=local_day).groupby(level=0).sum()
    daily = daily[(daily.index.year == year)]
    dates = daily.index

    rate = np.abs(np.gradient(el)) / step_h           # deg per hour
    speed = float(np.median(rate[band])) if band.any() else None

    return {
        "low_sun_hours": round(float(band.sum() * step_h), 1),
        "low_sun_fraction": round(float(band.sum() / above.sum()), 3) if above.any() else None,
        "median_daily_low_sun_min": int(np.median(daily[daily > 0])) if (daily > 0).any() else 0,
        "band_speed_deg_per_hr": round(speed, 2) if speed is not None else None,
        "best_window": longest_run((daily >= WINDOW_MIN_PER_DAY).to_numpy(), dates),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2027)
    ap.add_argument("--out", default="out/sun.json")
    args = ap.parse_args()

    sites = [s for s in json.load(open("data/sites.json")) if s["role"] != "moon"]
    out = {}
    for s in sites:
        r = site_sun(s["lat"], s["lon"], args.year)
        out[s["id"]] = r
        w = r["best_window"]
        wtxt = f"{w['start']} to {w['end']} ({w['days']} d)" if w else "none"
        print(f"{s['id']:15s} low-sun {r['low_sun_hours']:7.1f} h  fraction {r['low_sun_fraction']:.3f}  "
              f"speed {r['band_speed_deg_per_hr']} deg/h  best window {wtxt}")

    out["_moon"] = {
        "low_sun_fraction": 1.0,
        "note": "At the lunar south pole the Sun stays about 1-2 deg above the horizon "
                "(NASA lighting study, Litaker et al., NTRS 20240011393) and moves very slowly.",
    }
    os.makedirs("out", exist_ok=True)
    json.dump(out, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
