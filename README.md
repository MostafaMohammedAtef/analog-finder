# Analog Finder

Analog Finder is a four-person NASA Space Apps hackathon project that scores locations on Earth by how similar they are to a Moon or Mars target site.

## Repository ownership

- **Member 1 - Earth data:** `member1_earth_data/`; owns `data/earth_grid.csv`.
- **Member 2 - Science:** `member2_science/`; owns `data/targets.json`, `data/known_analogs.csv`, and slides.
- **Member 3 - Scoring:** `member3_scoring/`; owns the scoring and validation scripts.
- **Member 4 - Map UI:** `member4_map_ui/`; owns the Leaflet map.

## Data contract

Do not change column names without telling the team first.

- `data/earth_grid.csv` columns: `cell_id, lat, lon, slope_deg, elev_m, temp_range_k, ndvi, precip_mm_yr, dust_idx`
- `data/targets.json`: `{ "jezero": {"slope_deg": ..., "temp_range_k": ..., "ndvi": 0, "precip_mm_yr": 0, "dust_idx": ...}, "shackleton_rim": {...} }`
- `data/known_analogs.csv` columns: `name, lat, lon`
- `out/scores_<target>.csv` columns: `cell_id, lat, lon, score, sim_slope_deg, sim_temp_range_k, sim_ndvi, sim_precip_mm_yr, sim_dust_idx`

The checked-in data is intentionally fake demo data. Raw source data belongs in `data/raw/` and is ignored by git.

## Run the demo

```bash
pip install -r requirements.txt
python scripts/make_fake_data.py
python member3_scoring/score.py jezero
python -m http.server
```

Then open <http://localhost:8000/member4_map_ui/>.

To validate known analogs after generating scores:

```bash
python member3_scoring/validate.py jezero
```

## Project structure

See each member directory for its ownership boundary. `scripts/make_fake_data.py` regenerates the fake files in `data/`, and `out/` contains generated scores.
