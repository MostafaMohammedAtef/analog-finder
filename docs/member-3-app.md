# App lane (Member 3)

You own `web/`. A working starter is already there: map, ranking, weight sliders, site panel with radar chart, low-sun facts, temperature bar, works/breaks lists, and the "no Earth site can reproduce" panel.

## Run it locally

```bash
python -m http.server 8000 -d web      # Windows: py -m http.server 8000 -d web
```
Open http://localhost:8000. (Opening `index.html` directly from the file system won't load the JSON; use the server.)

The app loads `web/results.json` if it exists, otherwise `web/mock_results.json` and shows a "MOCK data" banner. No code change is needed to switch.

## Files

| File | What it does |
| --- | --- |
| `web/index.html` | Page layout |
| `web/app.js` | Loads data, draws map markers, ranking, panel, radar chart |
| `web/style.css` | Dark theme |
| `web/vendor/` | Leaflet and Chart.js bundled locally (works without a CDN) |
| `web/make_mock.py` | Rebuilds `mock_results.json` from `data/sites.json` + `content/breaks.json` |
| `web/mock_results.json` | FAKE numbers in the exact contract shape |

## Event day

| When | Do |
| --- | --- |
| H0-H1 | Run the app locally; confirm the mock loads. |
| H1-H12 | Polish the panel; add a legend for marker colours; show Moon-vs-Moon ceiling from `moon.windows`. |
| H12 | Sync: Member 1 runs `merge.py`; one real site must show. |
| H12-H24 | Turn on GitHub Pages (below). Make sure real data looks right. |
| H24-H36 | Stretch: slope histogram chart (site vs Moon) from `terrain.slope_hist`; mobile layout; "compare two sites". |
| H36+ | Screen-record the demo for the video. |

## Publish on GitHub Pages

The workflow `.github/workflows/pages.yml` publishes `web/` on every push to `main`.
One-time setup: repo **Settings -> Pages -> Source: GitHub Actions**. The URL appears in the Actions run.

## Ideas that impress judges

- A slope histogram overlay: the site's histogram vs the Moon's, so judges see why a score is high or low.
- The Moon-vs-Moon ceiling line on the radar chart ("best realistic score").
- Clicking Egypt's sites shows terrain matching but lighting failing: say it in one sentence at the top of the panel.
