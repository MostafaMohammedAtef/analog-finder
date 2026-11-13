# Analog Finder

**NASA Space Apps Challenge 2026: Identify Earth locations that are analogs for permanent Moon base locations**

Analog sites are usually picked by habit (Hawaii, Arizona, Iceland), not by measurement. Analog Finder scores Earth sites against the **lunar south pole**, where Artemis is going, using NASA data. For every site it shows **how well it matches, when it's best to test there, and where the match breaks down**.

## The problem

At the lunar south pole the Sun stays about 1-2 degrees above the horizon and barely moves. Shadows are long, glare is harsh, and the terrain is rough. Rovers, landers and crews must be tested on Earth first, but nobody can easily say which Earth site is most like this, or what each site gets wrong.

## What we measure

| Feature | Earth data | Moon data | Scored? |
| --- | --- | --- | --- |
| Slope (steepness) | NASA ASTER GDEM v3 (30 m) | LRO LOLA 5 m DEMs (Connecting ridge, Shackleton rim) | Yes |
| Roughness (150 m window) | NASA ASTER GDEM v3 | LRO LOLA | Yes |
| Low-sun lighting (0-5 deg) | Sun position maths (pvlib) | Sun stays ~1-2 deg up | Yes |
| How fast the Sun moves through that band | Sun position maths | Almost still | Shown |
| Temperature range | NASA MODIS land surface temperature (AppEEARS) | LRO Diviner | Shown, not scored |

Similarity = histogram intersection with the Moon reference (0 = nothing in common, 1 = identical). The two Moon windows are also scored against each other, which gives the realistic ceiling.

**What no Earth site can reproduce:** 1/6 gravity, vacuum, radiation, lunar temperature extremes, lunar regolith. The app says this openly.

## Sites (13 + 2 Moon windows)

Five famous analogs as a baseline, five less obvious candidates, and three sites in Egypt (Kamil Crater, the Black Desert, Gilf Kebir). See [`data/sites.json`](data/sites.json).

## Repo layout

```
constants.py            shared numbers - nobody changes after kickoff
data/sites.json         the 13 Earth sites + 2 Moon windows (frozen at H1)
data/dem/               downloaded DEMs (NOT committed - too big)
terrain/                Member 1: download_earth.py, terrain.py  -> out/terrain.json
sun/                    Member 2: sun.py -> out/sun.json; temp_tools.py -> out/temp.json
web/                    Member 3: the app (index.html, app.js, style.css, mock_results.json)
content/breaks.json     Member 4: why / works / breaks / access per site + the "no site can reproduce" list
merge.py                joins everything -> web/results.json (the app reads this)
out/                    each lane's JSON output (committed - small)
docs/                   one guide per member + timeline
scripts/check_contracts.py   checks every JSON file against CONTRACTS.md (run before each PR)
CONTRACTS.md            exact file formats - read before writing any output
CONTRIBUTING.md         team rules: branches, file ownership, syncs
CLAUDE.md               rules for AI assistants (Claude, Copilot, Cursor...) working in this repo
.github/                PR template, CODEOWNERS, contract check + GitHub Pages deploy workflows
```

## Quick start

```bash
# Windows: use "py" instead of "python"
python -m pip install -r requirements.txt

python sun/sun.py                       # works immediately, no downloads
python terrain/terrain.py --only svalbard   # after downloading DEMs (docs/member-1-terrain.md)
python merge.py                         # builds web/results.json
python -m http.server 8000 -d web       # open http://localhost:8000
```

The app shows mock data until `web/results.json` exists.

Before every pull request: `python scripts/check_contracts.py` (GitHub runs it too).

**Publishing the app (once):** repo Settings -> Pages -> Source: **GitHub Actions**. Every push to `main` then deploys `web/` automatically.

## Team

| Member | Lane | Guide |
| --- | --- | --- |
| 1 | Terrain + merge | [docs/member-1-terrain.md](docs/member-1-terrain.md) |
| 2 | Sun + temperature | [docs/member-2-sun-temp.md](docs/member-2-sun-temp.md) |
| 3 | App | [docs/member-3-app.md](docs/member-3-app.md) |
| 4 | Science + story | [docs/member-4-story.md](docs/member-4-story.md) |

Timeline and sync points: [docs/timeline.md](docs/timeline.md)

## Data sources

- LRO LOLA high-resolution south pole DEMs, Barker et al. 2021, *Planetary & Space Science* 203, 105119: https://pgda.gsfc.nasa.gov/products/78
- NASA ASTER GDEM v3 (ASTGTM v003), NASA Earthdata
- Copernicus DEM GLO-30 (ESA), cross-check
- NASA MODIS MOD11A2 land surface temperature via AppEEARS
- LRO Diviner lunar radiometer (PDS Geosciences)
- South pole lighting: Litaker et al., NASA NTRS 20240011393
