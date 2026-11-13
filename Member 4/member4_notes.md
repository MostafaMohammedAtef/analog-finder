# Member 4 working notes

## Problem statement (draft)

Astronauts and rovers bound for the lunar south pole will work in a landscape unlike anywhere humans have walked: cratered highlands lit by a Sun that hangs only a degree or two above the horizon, casting long shadows that never shorten. Teams train for this on Earth at "analog" sites, but those sites are usually chosen by reputation and photographs, not by measurement. We built the Lunar South Pole Analog Scorer, which compares 13 Earth sites against two real south-pole windows using NASA elevation data (slope and roughness from 30 m DEMs) and a full year of computed sun angles. Each site gets a transparent score, a best season for low-sun testing, and an honest list of what it gets right and what it cannot reproduce, so mission planners and students can choose, and question, the places we use to rehearse for the Moon.

## Kickoff: Worldview site check

Each link opens the exact 10 x 10 km window. Northern sites open on 15 July and southern sites on 15 January, because in November the high-latitude sites are in polar night and show up black.

Base layer is MODIS (250 m), which is too coarse to judge. In Worldview, click **Add Layers**, search **HLS**, and add the Landsat/Sentinel-2 (30 m) true-colour layer. If that day is cloudy, step the date back a few days.

Pass rule: mostly bare ground, no ice sheet, no town, no large water body.

| id | window | check | notes |
|---|---|---|---|
| haughton | [open](https://worldview.earthdata.nasa.gov/?v=-89.8579,75.3351,-89.5021,75.4249&t=2026-07-15) | **PASS** | Clear on 2026-07-17 (HLS). Bare tan-grey breccia ground cut by small valleys; small lakes and leftover gully snow only. No town, no ice sheet. Centre unchanged (75.38, -89.68) |
| sp_crater | [open](https://worldview.earthdata.nasa.gov/?v=-111.6852,35.5351,-111.5748,35.6249&t=2026-07-15) | | |
| meteor_crater | [open](https://worldview.earthdata.nasa.gov/?v=-111.0749,34.9851,-110.9651,35.0749&t=2026-07-15) | | Visitor centre is fine, not a town |
| mauna_kea | [open](https://worldview.earthdata.nasa.gov/?v=-155.5177,19.7151,-155.4223,19.8049&t=2026-07-15) | | Check the window is not mostly vegetated lower slope |
| atacama | [open](https://worldview.earthdata.nasa.gov/?v=-69.9692,-24.1249,-69.8708,-24.0351&t=2026-01-15) | | |
| svalbard | [open](https://worldview.earthdata.nasa.gov/?v=13.1047,79.4051,13.5953,79.4949&t=2026-07-15) | | **Likely problem:** fjord water and glaciers may sit inside the box. Move onto the Sverrefjell / land side if needed |
| peary_land | [open](https://worldview.earthdata.nasa.gov/?v=-30.3441,82.4551,-29.6559,82.5449&t=2026-07-15) | | Check for summer snow patches |
| dry_valleys | [open](https://worldview.earthdata.nasa.gov/?v=161.7925,-77.5449,162.2075,-77.4551&t=2026-01-15) | | **Likely problem:** Wright Valley glacier or lake ice. Move onto the bare valley floor or walls |
| holuhraun | [open](https://worldview.earthdata.nasa.gov/?v=-16.9358,64.8251,-16.7242,64.9149&t=2026-07-15) | | Box should be on the dark 2014-15 lava, not the surrounding sand |
| khaybar | [open](https://worldview.earthdata.nasa.gov/?v=39.8504,24.9551,39.9496,25.0449&t=2026-07-15) | | Box should be on lava, not on farms or the town |
| kamil | [open](https://worldview.earthdata.nasa.gov/?v=26.0396,21.9731,26.1364,22.0629&t=2026-07-15) | | Crater is 45 m across, roughly 1.5 HLS pixels; look for the ejecta rays |
| black_desert | [open](https://worldview.earthdata.nasa.gov/?v=28.6791,28.1051,28.7809,28.1949&t=2026-07-15) | | Box should include the dark-capped hills, not just flat plain |
| gilf_kebir | [open](https://worldview.earthdata.nasa.gov/?v=25.9511,23.1551,26.0489,23.2449&t=2026-07-15) | | Box should include a scarp edge, or there is no point in this site |

Flag for the whole team: Kamil's crater is 45 m across, which is about 1.5 pixels at 30 m, so the DEM barely sees it. Keep Kamil in the list, since it is the demo for "matches by eye, fails at mission scale," and say so on the honesty panel.

## Judging criteria to demo

| Criterion | What judges look for | Where we show it |
|---|---|---|
| Impact | Who it helps and how much | Opening: mission planners, analog-site selection, Egyptian students and field teams |
| Creativity | A new angle | Scoring analog sites on low-sun lighting, not just terrain; Egypt as a terrain-match, lighting-fail case |
| Validity | Is the science sound? | README methodology, honesty panel, `cannot_reproduce` panel, H24/H36 checks that the numbers make sense |
| Relevance | Responds to the challenge | Uses NASA data: LOLA, ASTER GDEM, MODIS LST, Diviner, Worldview |
| Presentation | Clear demo and video | Map, then a click on Svalbard, then a click on Kamil to contrast them, then the honesty panel; 30 s per beat |

Confirm the exact wording in the current Judging & Awards Guide (spaceappschallenge.org/resources/judging-awards-guide).

## Sense checks for H24 and H36

- `low_sun_fraction`: Peary Land > Svalbard > Haughton > Holuhraun, which are all well above the Egypt, Arizona, Mauna Kea and Khaybar sites. Mauna Kea should be the lowest.
- Moon windows: `low_sun_fraction` should be close to 1.
- `slope_p90_deg`: Gilf Kebir and SP Crater should be high; Atacama and Black Desert should be low.
- `slope_similarity` and `roughness_similarity` must stay between 0 and 1.
- Every site id appears in every file, with `null` for missing values, not a missing key.
