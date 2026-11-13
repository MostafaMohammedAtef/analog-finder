# Stretch (after H24 only): radar comparison for one site

**Why it's interesting.** Canada's RADARSAT Constellation Mission (RCM) transmits circular polarization and receives H and V. NASA's LRO Mini-RF radar uses the same "hybrid-polarity" idea. Both can give a **circular polarization ratio (CPR)**, a standard measure of how rough a surface is at the scale of the radar wavelength (centimetres to decimetres). That's a roughness scale our 30 m DEMs can't see, so it fills a gap we admit on the honesty panel.

**Why it's only a stretch.**
- RCM open data doesn't cover every site; check the CSA catalogue for scenes over your sites first (link in the challenge resources).
- RCM is C-band (about 5.6 cm wavelength); Mini-RF is longer wavelength, so CPR values are not directly comparable. Present it as a qualitative comparison, and say so.
- Sentinel-1 (ESA, Copernicus) is easier to get but uses linear polarization only, so it gives backscatter brightness, not CPR.

**Minimal version (2-4 hours, one person).**
1. Find one RCM compact-pol scene over one site (a polar site or Black Desert).
2. Open it in QGIS using the CSA tutorial from the challenge resources (github.com/asc-csa/Synthetic_Aperture_Radar_Tutorial).
3. Compute CPR for the 10 x 10 km window; find a Mini-RF CPR map of the south pole on the PDS.
4. Show the two side by side in the app or the video, with one sentence on what matches and what doesn't.

If no RCM scene covers a site, drop this and say so in the README.
