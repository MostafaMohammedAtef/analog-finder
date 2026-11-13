# 48-hour timeline

H0 = your local event start on Nov 14, 2026. All four lanes run at the same time from H1.

| Phase | Hours | Terrain (1) | Sun + temp (2) | App (3) | Story (4) |
| --- | --- | --- | --- | --- | --- |
| Kickoff | H0-H1 | Commit constants + sites; check Moon DEMs open | Confirm constants | Mock loads locally | Check site centres on Worldview |
| One site | H1-H12 | Svalbard + Moon -> `terrain.json`; run `merge.py` | `sun.json` all sites by H4 | Panel polish on mock data | `breaks.json` first 3 sites |
| All sites | H12-H24 | All 13 sites | `temp.json` Earth + Moon | Real data; GitHub Pages live | All sites; README draft |
| Polish | H24-H36 | Fix outliers; help app | Stretch: horizon, snow | Stretch: histograms, ceiling | Sanity check; project page |
| Video + submit | H36-H48 | Final numbers to README | Check figures for video | Screen-record demo | Edit video; submit by H46 |

## Gates (15-minute syncs)

| Gate | Must be true |
| --- | --- |
| H1 | `constants.py`, `data/sites.json`, `CONTRACTS.md` merged into `main`; everyone on their branch |
| H6 | Check-in: each lane done / next / blocked |
| **H12** | **One real site shows in the app end to end** |
| H24 | All numbers real; app online on GitHub Pages |
| H36 | Feature freeze: only fixes and the video after this |
| H46 | Submitted (2 h buffer) |

If a lane misses a gate, the others keep working on mock or partial data; the late lane catches up by the next gate.

## Stretch, only after H24

- Horizon-shaded sun (Member 2), slope histogram overlay (Member 3).
- Radar backscatter showcase for one site (see [stretch-sar.md](stretch-sar.md)).
