# Data contracts

Each file has **one owner**. Nobody edits another member's file. Every per-site file is keyed by the `id` in `data/sites.json`. A missing value is `null`, never a missing key, so the app always loads.

| File | Owner | Read by | 1 site ready | All sites |
| --- | --- | --- | --- | --- |
| `data/sites.json` | All (frozen at H1) | everyone | H1 | H1 |
| `constants.py` | All (frozen at H1) | everyone | H1 | H1 |
| `web/mock_results.json` | Member 3 | the app | H1 | H1 |
| `out/terrain.json` | Member 1 | merge.py | H10 | H22 |
| `out/sun.json` | Member 2 | merge.py | H4 | H8 |
| `out/temp.json` | Member 2 | merge.py | H12 | H22 |
| `content/breaks.json` | Member 4 | merge.py | H8 | H20 |
| `web/results.json` | merge.py (Member 1 runs it) | the app | H12 | H24 |

## Shared constants (`constants.py`)

- Window 10 x 10 km; every DEM resampled to 30 m.
- Slope bins: 0-45 deg, 1 deg steps (45 bins); steeper goes in the last bin.
- Roughness: std of elevation in a 5 x 5 pixel (150 m) window. Bins 0-20 m, 1 m steps (20 bins).
- Similarity: histogram intersection, sum(min(p, q)), each histogram normalised to sum 1. Range 0-1.
- Low-sun fraction: time with sun elevation between 0 and 5 deg / all time with the Sun up. One year, 10-minute steps, flat horizon.
- Overall score: weighted mean of slope, roughness and low-sun (default weights 1, 1, 1; the app lets users change them).

## Shapes

`out/terrain.json` (Member 1). Moon windows appear too; their similarity is against the *other* Moon window (the ceiling).
```json
{"svalbard": {"slope_hist": [45 numbers], "rough_hist": [20 numbers],
  "slope_similarity": 0.71, "roughness_similarity": 0.64,
  "slope_p50_deg": 4.1, "slope_p90_deg": 18.2, "rough_p50_m": 2.3, "relief_m": 610,
  "valid_fraction": 0.99, "window_km": 9.99}}
```

`out/sun.json` (Member 2)
```json
{"svalbard": {"low_sun_hours": 710.0, "low_sun_fraction": 0.156, "median_daily_low_sun_min": 270,
  "band_speed_deg_per_hr": 1.74, "best_window": {"start": "08-12", "end": "10-21", "days": 71}},
 "_moon": {"low_sun_fraction": 1.0, "note": "..."}}
```
`best_window` is `null` when there is no run of days with at least 2 h of low sun.

`out/temp.json` (Member 2)
```json
{"svalbard": {"lst_min_c": -32.5, "lst_max_c": 21.0},
 "_moon": {"min_c": null, "max_c": null, "source": "Diviner (LRO)"}}
```

`content/breaks.json` (Member 4)
```json
{"_global": ["what no Earth site can reproduce", "..."],
 "svalbard": {"why": "...", "works": ["..."], "breaks": ["..."], "access": "..."}}
```

`web/results.json` (written by merge.py; `web/mock_results.json` has the same shape plus `"mock": true`)
```json
{"sites": [{"id": "svalbard", "name": "...", "lat": 79.45, "lon": 13.35, "role": "candidate",
   "scores": {"slope": 0.71, "roughness": 0.64, "low_sun": 0.156, "overall": 0.50},
   "terrain": {"slope_p50_deg": 4.1, "slope_p90_deg": 18.2, "rough_p50_m": 2.3, "relief_m": 610,
               "slope_hist": [], "rough_hist": []},
   "best_window": {"start": "08-12", "end": "10-21", "days": 71},
   "sun": {"low_sun_hours": 710.0, "low_sun_fraction": 0.156, "median_daily_low_sun_min": 270,
           "band_speed_deg_per_hr": 1.74},
   "temp": {"min_c": -32.5, "max_c": 21.0},
   "why": "...", "works": [], "breaks": [], "access": "..."}],
 "moon": {"windows": {"moon_connecting_ridge": {}}, "temp": {}, "sun": {}},
 "cannot_reproduce": ["..."],
 "weights": {"slope": 1.0, "roughness": 1.0, "low_sun": 1.0}}
```

**Changing a contract** after H1 needs all four people to agree at a sync, and the owner updates this file in the same pull request.
