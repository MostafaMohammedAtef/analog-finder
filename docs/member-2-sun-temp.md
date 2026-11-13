# Sun and temperature lane (Member 2)

You produce `out/sun.json` (low-sun lighting per site) and `out/temp.json` (Earth vs Moon temperature range).

## Files

| File | What it does |
| --- | --- |
| `sun/sun.py` | Sun position every 10 minutes for a year, per site -> `out/sun.json` |
| `sun/temp_tools.py` | `points`: makes the AppEEARS upload file. `convert`: turns AppEEARS results into `out/temp.json` |

## Tonight

1. `python -m pip install -r requirements.txt` (Windows: `py -m pip ...`)
2. `python sun/sun.py` - takes a few seconds, no downloads. Check the printout looks sensible (see below).
3. Make a NASA Earthdata account, then submit the temperature request **tonight** (AppEEARS queues requests):
   - `python sun/temp_tools.py points` -> `sun/appeears_points.csv`
   - Go to https://appeears.earthdatacloud.nasa.gov -> Extract -> Point Sample -> upload that CSV
   - Product **MOD11A2** (MODIS land surface temperature, 8-day, 1 km), layers `LST_Day_1km` and `LST_Night_1km`
   - Dates 2025-01-01 to 2025-12-31 -> Submit

## Event day

| When | Do |
| --- | --- |
| H0-H1 | Confirm `constants.py` matches CONTRACTS.md. |
| H1-H4 | Run `python sun/sun.py`, push `out/sun.json` on your `sun` branch. Done early: help Member 3 or 4. |
| H4-H12 | When AppEEARS emails you: download the CSV into `sun/`, run `python sun/temp_tools.py convert sun/<file>.csv`. |
| H12-H22 | Moon temperatures from Diviner for the two Moon windows -> fill `"_moon"` in `out/temp.json` with `min_c`, `max_c` and `source`. |
| H24-H36 | Stretch: horizon shading from Member 1's DEM windows; MODIS snow cover during each best window. |

## What the sun numbers mean

- `low_sun_fraction` - share of daylight with the Sun 0-5 deg up. The Moon reference is about 1.0.
- `band_speed_deg_per_hr` - how fast the Sun moves through that band. At the lunar pole it barely moves; mid-latitude sites cross it in minutes. This is the clearest way to show why Egypt fails on lighting.
- `best_window` - longest run of days with at least 2 h of low sun: the best dates to test there. `null` = no such run.

## Sanity checks (first real run, 2027, flat horizon)

| Site | Low-sun fraction | Band speed | Best window |
| --- | --- | --- | --- |
| Svalbard | 0.156 | 1.7 deg/h | Aug 12 to Oct 21 |
| Peary Land | 0.152 | 1.3 deg/h | Aug 21 to Oct 13 |
| Kamil (Egypt) | 0.068 | 13.0 deg/h | none |
| Mauna Kea | 0.068 | 13.2 deg/h | none |

## Limits to state honestly (give to Member 4)

- Flat horizon: real mountains block the low Sun. The stretch task fixes this with DEM horizons.
- Earth's atmosphere scatters light and brightens shadows; the Moon has none.
- Snow can cover polar sites during their best windows.
