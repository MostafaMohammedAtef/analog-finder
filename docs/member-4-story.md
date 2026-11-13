# Science and story lane (Member 4)

You own `content/breaks.json`, `docs/`, the README, the Space Apps project page and the demo video. You are also the team's quality checker.

## Tonight

1. Read the official submission and judging guides (released Nov 13). Write down every judging criterion and which part of the demo answers it.
2. Draft the one-paragraph problem statement (start from README.md).
3. Review the `_global` list in `content/breaks.json`.

## Event day

| When | Do |
| --- | --- |
| H0-H1 | Check each site centre on NASA Worldview (https://worldview.earthdata.nasa.gov): the 10 x 10 km window should be bare ground, no ice sheet, no town. Tell Member 1 before H1 if a centre moves. |
| H1-H8 | Fill `why`, `access`, `works`, `breaks` for the first 3 sites (Svalbard, Kamil, Black Desert). Run `python web/make_mock.py` to see them in the app. |
| H8-H20 | All 13 sites. |
| H20-H24 | README methodology: data, metrics, limits, how this differs from earlier work (below). |
| H24, H36 | Sanity-check the numbers with the team (Member 1 and 2 guides list expected values). |
| H24-H36 | Space Apps project page text. |
| H36-H46 | Record and edit the demo video; submit by H46. |

## Writing works / breaks

Each bullet: one short sentence, specific, ideally with a number from the app.
- Works: "Slope distribution matches the Shackleton rim window at 0.62."
- Breaks: "The Sun crosses the 0-5 deg band at 13 deg/h, about 10 times faster than at Svalbard; shadows don't hold still like on the Moon."

## How this differs from earlier work (for the README and pitch)

- Earlier work ranked Earth sites by **image texture** (how photos look). We use **physical elevation data** (slope and roughness from DEMs) plus **sun geometry**.
- We report **where each analogy fails**, per feature, and what no Earth site can reproduce.
- We include under-used sites, including three in Egypt.

## Limits to state (collect from Members 1 and 2)

- 30 m pixels: landscape-scale terrain, not single rocks.
- Flat-horizon sun model (unless the stretch task is done).
- ASTER (stereo images) and LOLA (laser) are different instruments.
- Temperature shown, not scored: no Earth site comes close.
- Moon reference = two windows near Artemis candidate sites, not the whole south pole.

## Pitch line

"Analog sites are picked by habit. We measure them against the lunar south pole with NASA data, and show where each match works and where it fails."
