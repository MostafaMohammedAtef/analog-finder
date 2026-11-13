# Rules for AI assistants working in this repo

Read this before changing anything. It also applies to Copilot, Cursor, ChatGPT and other tools.

## What this project is

Analog Finder scores 13 Earth sites against the lunar south pole (slope, roughness, low-sun lighting) for NASA Space Apps 2026. Each site shows how well it matches and where the match breaks. See `README.md`.

## Hard rules

1. **Stay in the lane of the person you're helping.** Ask which member they are if it's unclear. Only edit that lane's files (table in `CONTRIBUTING.md`). Never edit another lane's files, even to "fix" them; suggest the change instead.
2. **Never change frozen files** (`constants.py`, `data/sites.json`, `CONTRACTS.md`) unless the user says the whole team agreed at a sync.
3. **Follow `CONTRACTS.md` exactly.** Same keys, same nesting, `null` for missing values (never drop a key). Run `python scripts/check_contracts.py` after writing any output file.
4. **Never invent data.** No made-up temperatures, coordinates, scores or citations. If a value isn't measured yet, it is `null`. Mock numbers live only in `web/mock_results.json` (which says `"mock": true`).
5. **Never commit large or secret files:** DEMs, `.tif`, raw downloads, `.netrc`, tokens. They are in `.gitignore`; don't work around it.
6. **Work on the lane branch** (`terrain`, `sun`, `app`, `story`), never directly on `main`.
7. **Keep it runnable on Windows.** Use `os.path` and paths relative to the repo root; scripts already `chdir` to the root. Commands in docs show both `python` and `py`.
8. **No new dependencies** without adding them to `requirements.txt` and telling the user. The web app has no build step and loads libraries from `web/vendor/` (no CDN), so keep it that way.
9. **Be honest in the science.** Where a site fails, say so in `content/breaks.json`. Don't tune methods to make a favourite site win.

## Where things are

| Path | Owner | Purpose |
| --- | --- | --- |
| `terrain/` | Member 1 | DEM download + slope/roughness -> `out/terrain.json` |
| `merge.py` | Member 1 | all lanes -> `web/results.json` |
| `sun/` | Member 2 | sun angles -> `out/sun.json`; MODIS temperatures -> `out/temp.json` |
| `web/` | Member 3 | static app (Leaflet + Chart.js), reads `results.json` else `mock_results.json` |
| `content/`, `docs/`, `README.md` | Member 4 | per-site why/works/breaks/access, methodology, pitch |

## Checks before you say "done"

- `python scripts/check_contracts.py` passes.
- `python merge.py` runs and the app loads: `python -m http.server 8000 -d web`.
- No file over 5 MB is staged: `git status` and check.
