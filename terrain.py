# Terrain lane (Member 1)

You produce `out/terrain.json` (slope and roughness similarity to the lunar south pole for every site) and you own `merge.py`, which builds `web/results.json` for the app.

## Files

| File | What it does |
| --- | --- |
| `constants.py` | Shared numbers (10 km window, 30 m grid, bins, weights). Commit to `main` at kickoff. |
| `data/sites.json` | 13 Earth sites + 2 Moon windows. Commit to `main` at kickoff. |
| `download_earth.py` | Downloads Earth DEM tiles into `data/dem/earth/<site_id>/` |
| `terrain.py` | Builds every 10 x 10 km window, computes slope and roughness, writes `out/terrain.json` |
| `merge.py` | Joins all lanes' files into `web/results.json` |

## Tonight (about 1 hour)

1. Install:
   `pip install rasterio pyproj scipy numpy earthaccess`
2. Make a free NASA Earthdata account: https://urs.earthdata.nasa.gov
3. Download the two Moon files (small 5 m/pixel GeoTIFFs from NASA Goddard) into `data/dem/moon/`:
   - Site01 Connecting ridge: `Site01_final_adj_5mpp_surf.tif`
   - Site04 Shackleton rim: `Site04_final_adj_5mpp_surf.tif`
   - Page: https://pgda.gsfc.nasa.gov/products/78
   - Don't download the 3.3 GB 87-90 S mosaic; you don't need it.
4. Download Earth tiles. Try one site first:
   `python download_earth.py --only svalbard`
   then all sites:
   `python download_earth.py`
   If Earthdata login or ASTER gives trouble, use the no-login fallback:
   `python download_earth.py --source copernicus`
5. Test with one site:
   `python terrain.py --only svalbard`
   You should see two `moon ... ok` lines and one Earth line with scores.

## Event day

| When | Do |
| --- | --- |
| H0-H1 | Commit `constants.py` + `data/sites.json` to `main`. Open each Moon file in QGIS and check it shows a ridge/rim (not blank). |
| H1-H10 | `python terrain.py --only svalbard`, then push `out/terrain.json` on your `terrain` branch. Run `python merge.py` so the app has real numbers for one site. |
| H10-H22 | `python terrain.py` for all 13 sites. Fix any site marked SKIPPED or "low coverage". |
| H12 | Sync: one site must show up in the app end to end. |
| H22-H36 | Look for odd numbers (see checks below), help Member 3 if needed. |
| H36+ | Freeze numbers; give Member 4 the final table for the README. |

## How the scores work (for the README and the judges)

- Every DEM is cut to the same 10 x 10 km window and resampled to 30 m. Earth goes to local UTM; the Moon stays in its south polar stereographic grid (5 m averaged up to 30 m).
- **Slope** = steepness of each 30 m pixel, in degrees. **Roughness** = standard deviation of elevation in a 150 m (5 x 5 pixel) window.
- Each site's slope and roughness are turned into histograms (share of the window in each bin).
- **Similarity** = histogram intersection with the Moon reference (the average of the two Moon windows): 0 = nothing in common, 1 = identical.
- The two Moon windows are also scored against each other. That number is the realistic ceiling: if two real lunar sites only match at 0.5, an Earth site at 0.4 is a strong match.

## Sanity checks before you trust the numbers

- `valid_fraction` should be close to 1. Below 0.9 means missing tiles or ocean in the window: move the site centre a little (tell Member 4).
- Flat sites (Atacama plain, Kamil surroundings) should have low slope p90; Mauna Kea, Gilf Kebir scarps and Haughton rim should be higher.
- If every Earth site scores near 0, check the Moon windows loaded (not blank) and that elevation units are metres.
- ASTER GDEM has spikes and pits over snow and steep shadows. If a polar site looks wild, compare with `--source copernicus`.

## Limits to state honestly (give these to Member 4)

- 30 m pixels capture landscape-scale terrain (landing zones, routes), not individual rocks under a rover's wheels.
- ASTER GDEM and LOLA are built differently (stereo images vs laser), so small differences in roughness partly reflect the instruments.
- The Moon reference is two windows near Artemis candidate sites, not the whole south pole.
