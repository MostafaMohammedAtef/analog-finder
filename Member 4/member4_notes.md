# Member 4 working notes

## Problem statement (draft)

Astronauts and rovers bound for the lunar south pole will work in a landscape unlike anywhere humans have walked: cratered highlands lit by a Sun that hangs only a degree or two above the horizon, casting long shadows that never shorten. Teams train for this on Earth at "analog" sites, but those sites are usually chosen by reputation and photographs, not by measurement. We built the Lunar South Pole Analog Scorer, which compares 13 Earth sites against two real south-pole windows using NASA elevation data (slope and roughness from 30 m DEMs) and a full year of computed sun angles. Each site gets a transparent score, a best season for low-sun testing, and an honest list of what it gets right and what it cannot reproduce, so mission planners and students can choose, and question, the places we use to rehearse for the Moon.

## Kickoff: Worldview site check

Each link opens the exact 10 x 10 km window around the **final** centre (after the moves below). Northern sites open on 15 July and southern sites on 15 January, because in November the high-latitude sites are in polar night and show up black.

Base layer is MODIS (250 m), which is too coarse to judge. In Worldview, click **Add Layers**, search **HLS**, and add the Landsat/Sentinel-2 (30 m) true-colour layer. If that day is cloudy, step the date back a few days.

Pass rule: mostly bare ground, no ice sheet, no town, no large water body.

| id | window | check | notes |
|---|---|---|---|
| haughton | [open](https://worldview.earthdata.nasa.gov/?v=-89.8579,75.3351,-89.5021,75.4249&t=2026-07-15) | **PASS** | Clear on 2026-07-17 (HLS). Bare tan-grey breccia ground cut by small valleys; small lakes and leftover gully snow only. No town, no ice sheet. Centre unchanged (75.38, -89.68) |
| sp_crater | [open](https://worldview.earthdata.nasa.gov/?v=-111.6852,35.5551,-111.5748,35.6449&t=2026-07-15) | **PASS, nudge north** | Clear enough on 2026-07-16 (Landsat HLS, scattered monsoon cumulus). SP cone sits right at the old centre; its dark lava flow runs ~7 km north, so the old box cut off the top of the flow and was mostly tan plain. No town, only dirt tracks. **New centre: 35.60, -111.63**. June is clearer than July here (monsoon) |
| meteor_crater | [open](https://worldview.earthdata.nasa.gov/?v=-111.0749,34.9851,-110.9651,35.0749&t=2026-07-15) | **PASS** | Clear on 2026-07-20 (Sentinel-2 HLS, scattered cumulus). Crater bowl and light rim sit dead centre. Bare tan scrub desert, dirt tracks, no town; I-40 is ~9 km north, outside the box. Centre unchanged (35.03, -111.02). Crater is a small part of the 10 km box, so the window is mostly flat plain (already noted in breaks.json) |
| mauna_kea | [open](https://worldview.earthdata.nasa.gov/?v=-155.5177,19.7351,-155.4223,19.8249&t=2026-07-15) | **PASS, nudge north** | Checked 2026-07-20 (Sentinel-2 HLS, trade-wind cloud on the east side). Upper half of box is bare tan/red cinder cones and tephra; lower-right ~20% is green vegetated slope plus cloud. Pohakuloa Training Area camp sits just outside the west edge. **New centre: 19.78, -155.47** (box 19.735-19.825): shifts out of the green band, takes in the summit cinder cones; observatories are fine (not a town), Hale Pohaku ISRU test area stays inside |
| atacama | [open](https://worldview.earthdata.nasa.gov/?v=-69.9692,-24.1049,-69.8708,-24.0151&t=2026-01-15) | **PASS, nudge north** | Clear on 2026-07-19 (Sentinel-2 HLS). Bare pale hills and alluvial valleys, no vegetation. A cluster of white rectangular man-made structures (facility / panels) sits on the bottom edge of the box and runs south. Coastal cloud bottom-left and swath edge on the right are outside the box. **New centre: -24.06, -69.92** (box -24.105 to -24.015): clears the structures and adds more hill relief. Re-checked on the same image: new box is bare hills and valleys plus one dirt track; the northernmost small structure sits right on the bottom edge, everything else is outside |
| svalbard | [open](https://worldview.earthdata.nasa.gov/?v=13.3049,79.3951,13.7951,79.4849&t=2026-07-15) | **MOVED, marginal pass** | HLS unusable here (Worldview geographic view stretched ~5x at 79N; Arctic view has no HLS), so checked on Google Maps satellite with a 5 km ruler. Old centre (79.45, 13.35) sits at the head of a fjord arm: ~1/3 of the box was water, plus glacier/snowfield in the SW. **New centre: 79.44, 13.55** (picked on the dark ridged land wedge, Google Maps right-click 79.438466, 13.546904). Expect roughly 20% water at the box edges (fjord along the east and a thin strip at the top) and snow in gullies. Not re-measured with the ruler; flag on honesty panel |
| peary_land | [open](https://worldview.earthdata.nasa.gov/?v=-30.3441,82.4551,-29.6559,82.5449&t=2026-07-15) | **PASS** | Checked on Google Maps satellite (no HLS in polar view). Whole box is bare, dissected plateau of flat-lying sedimentary layers (ring patterns on mesas and buttes), steep valley walls, thin snow lines only. No ice cap, no sea, no buildings. Centre unchanged (82.50, -30.00) |
| dry_valleys | [open](https://worldview.earthdata.nasa.gov/?v=161.7925,-77.5449,162.2075,-77.4551&t=2026-01-15) | **PASS** | Checked on Google Maps satellite (2 km bar ~72 px, so box ~360 px square around pin). Box is dark bare valley floor plus rocky ridges with snow patches (~15%). Two ice-covered lakes and a glacier tongue sit just outside the box (west, north, south-east). Centre unchanged (-77.50, 162.00) |
| holuhraun | [open](https://worldview.earthdata.nasa.gov/?v=-16.9358,64.8251,-16.7242,64.9149&t=2026-07-15) | **PASS** | Google Maps satellite. Pin sits on the western edge of the very dark 2014-15 lava; east half of box is fresh lava, west half older greyer lava and sand plain. Glacier (Dyngjujokull) and river are just outside the box. Centre unchanged (64.87, -16.83) |
| khaybar | [open](https://worldview.earthdata.nasa.gov/?v=39.8504,25.0151,39.9496,25.1049&t=2026-07-15) | **FAIL → MOVED north** | Google Maps satellite. Old box was ~60% pale sand basin, with lava only along the top edge and dark hills in the SE corner. **New centre: 25.06, 39.90** (~7 km north) onto the dark lava field; bottom ~15% may still be sand. Archaeological stone-structure site to the east stays outside. **Confirmed in Worldview HLS (2026-08-13):** new box is dark lava with pale patches, pale basin only along the bottom edge |
| kamil | [open](https://worldview.earthdata.nasa.gov/?v=26.0396,21.9731,26.1364,22.0629&t=2026-07-15) | **PASS, note border** | Google Maps satellite. Bare orange sand with dark sandstone ridges and wind streaks, no structures. The 45 m crater is invisible at 10 km scale, as expected. **The Egypt-Sudan border (22.0 N) crosses the box: ~40% of the window lies in Sudan.** Kept crater-centred (22.018, 26.088); stated in access text |
| black_desert | [open](https://worldview.earthdata.nasa.gov/?v=28.6791,28.1051,28.7809,28.1949&t=2026-07-15) | **PASS** | Google Maps satellite. Tan desert with scattered dark-capped hills; Bahariya-Farafra road crosses the box (fine). Black Desert park marker just north, a tourist camp just east, centre-pivot farms on both sides, all outside. Centre unchanged (28.15, 28.73) |
| gilf_kebir | [open](https://worldview.earthdata.nasa.gov/?v=25.8211,23.1551,25.9189,23.2449&t=2026-07-15) | **MOVED west** | Google Maps satellite. Old box was mostly sand plain with dark knobs; the main serrated scarp edge sat 5-10 km west, outside it. **New centre: 23.20, 25.87** (~13 km west): Google Maps and Worldview HLS (2026-08-12) both put the serrated scarp edge at about 25.86-25.87 E, so the box now straddles it: low sand plain on the west half, dissected plateau on the east half, the full slope range this site is in for |

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
