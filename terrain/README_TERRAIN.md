# Terrain lane (Member 1)

You produce `out/terrain.json` (slope and roughness similarity to the lunar south pole **and to Mars** for every site) and you own `merge.py`, which builds `web/results.json` for the app.

## Files

| File | What it does |
| --- | --- |
| `constants.py` | Shared numbers (10 km window, 30 m grid, bins, weights). Commit to `main` at kickoff. |
| `data/sites.json` | 13 Earth sites + 2 Moon windows + 2 Mars windows. Commit to `main` at kickoff. |
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
- The two Moon windows are also scored against each other (about 0.42 with the real LOLA files). This is **not** a ceiling: Earth sites are compared with the *average* of both windows, so they can score higher (Mauna Kea and the Dry Valleys do). What it shows is that the south pole itself varies a lot: the ridge (p90 slope about 19 deg) and Shackleton's rim (about 33 deg) are very different ground. A high Earth score means the site sits in the middle of that range.

## Mars

Same method, second reference world. Each Earth site gets a Moon score **and** a Mars score.

**Data (one file, 87 MB):** the USGS Mars 2020 Science Investigation CTX DEM mosaic of Jezero crater
(20 m/pixel, covers the whole crater). Download it in your browser and save it as
`data/dem/mars/M20_JezeroCrater_CTXDEM_20m.tif`:
https://planetarymaps.usgs.gov/mosaic/mars2020_trn/CTX/ScienceInvestigationMaps_JPL/M20_JezeroCrater_CTXDEM_20m.tif
(product page: https://astrogeology.usgs.gov/search/map/mars_2020_science_investigation_ctx_dem_mosaic)

**Two Mars windows** (in `data/sites.json`, chosen to mirror the Moon pair: a lower, gentler area and a crater rim):
- `mars_jezero_delta`: delta and crater floor near Perseverance's landing site (18.47 N, 77.40 E)
- `mars_jezero_rim`: Jezero's western rim (18.40 N, 77.20 E)

The centres are approximate. If `terrain.py` prints "low coverage" for one, or its p90 slope looks too
gentle for a rim, nudge the lat/lon a few hundredths of a degree and rerun.

**How it differs from the Moon:**
- The Mars file is in an equirectangular projection, which stretches east-west distances by about 5% at
  Jezero's latitude. `terrain.py` cuts each Mars window on a local Transverse Mercator grid, so slopes
  are measured in true metres (tested: a 10-degree plane measures 10.0 degrees in every direction).
- Mars has **no low-sun score**. Jezero gets normal sunrises and sunsets, so the Mars overall score is
  the mean of slope and roughness only.
- Mars elevation comes from CTX stereo images (20 m), the Moon from laser altimetry (5 m) and Earth from
  radar (30 m). All are resampled to the same 30 m grid, but some roughness difference comes from the
  instruments.

**Outputs:**
- `out/terrain.json`: every site gains `mars_slope_similarity` and `mars_roughness_similarity`.
  Moon windows also get a Mars score, and Mars windows a Moon score (Moon vs Mars terrain, for interest).
- `web/results.json`: every site keeps `scores` (Moon, unchanged) and gains
  `scores_mars: {slope, roughness, overall}`; there is a new top-level `mars.windows` block.
  Member 3 can add a Moon/Mars toggle that switches which block colours the map and the radar chart.
- If the Mars file is missing, everything still runs and the Mars scores are `null`.

`merge.py --out ../results.json` writes the merged file next to the app's `index.html`.

## Sanity checks before you trust the numbers

- `valid_fraction` should be close to 1. Below 0.9 means missing tiles or ocean in the window: move the site centre a little (tell Member 4).
- Flat sites (Atacama plain, Kamil surroundings) should have low slope p90; Mauna Kea, Gilf Kebir scarps and Haughton rim should be higher.
- If every Earth site scores near 0, check the Moon windows loaded (not blank) and that elevation units are metres.
- ASTER GDEM has spikes and pits over snow and steep shadows. If a polar site looks wild, compare with `--source copernicus`.

## Limits to state honestly (give these to Member 4)

- 30 m pixels capture landscape-scale terrain (landing zones, routes), not individual rocks under a rover's wheels.
- ASTER GDEM and LOLA are built differently (stereo images vs laser), so small differences in roughness partly reflect the instruments.
- The Moon reference is two windows near Artemis candidate sites, not the whole south pole.
- The Mars reference is two windows in one crater (Jezero), not all of Mars.
