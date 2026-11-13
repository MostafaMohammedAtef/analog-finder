"""Download Earth DEM tiles for every Earth site into data/dem/earth/<site_id>/.

Default source: NASA ASTER GDEM v3 (ASTGTM v003) via the `earthaccess` library.
  It needs a free NASA Earthdata login; you'll be asked for it the first time.
Fallback: --source copernicus downloads Copernicus GLO-30 tiles from the public
  AWS bucket (no login needed).

Usage:
  python terrain/download_earth.py                     # all Earth sites, ASTER
  python terrain/download_earth.py --only svalbard     # one site
  python terrain/download_earth.py --source copernicus
"""
import argparse
import json
import math
import os
import sys
import urllib.request

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
os.chdir(_ROOT)  # all paths below are relative to the repo root
from constants import WINDOW_M


def site_bbox(lat, lon, margin_m=1_000):
    """Lon/lat box that safely contains the 10 x 10 km window (+ a margin)."""
    half = WINDOW_M / 2 + margin_m
    dlat = half / 111_320
    dlon = half / (111_320 * max(math.cos(math.radians(lat)), 0.05))
    return lon - dlon, lat - dlat, lon + dlon, lat + dlat


def tiles_for_bbox(w, s, e, n):
    """Integer 1x1-degree tile corners (lat, lon) touched by the box."""
    return [(la, lo)
            for la in range(math.floor(s), math.floor(n) + 1)
            for lo in range(math.floor(w), math.floor(e) + 1)]


def download_aster(site, out_dir):
    import earthaccess
    w, s, e, n = site_bbox(site["lat"], site["lon"])
    results = earthaccess.search_data(short_name="ASTGTM", version="003",
                                      bounding_box=(w, s, e, n))
    if not results:
        print(f"  ! no ASTER tiles found for {site['id']}")
        return []
    return earthaccess.download(results, out_dir)


def download_copernicus(site, out_dir):
    w, s, e, n = site_bbox(site["lat"], site["lon"])
    got = []
    for la, lo in tiles_for_bbox(w, s, e, n):
        ns = f"N{la:02d}" if la >= 0 else f"S{-la:02d}"
        ew = f"E{lo:03d}" if lo >= 0 else f"W{-lo:03d}"
        name = f"Copernicus_DSM_COG_10_{ns}_00_{ew}_00_DEM"
        url = f"https://copernicus-dem-30m.s3.amazonaws.com/{name}/{name}.tif"
        dest = os.path.join(out_dir, f"{name}.tif")
        if os.path.exists(dest):
            got.append(dest)
            continue
        try:
            print(f"  downloading {name} ...")
            urllib.request.urlretrieve(url, dest)
            got.append(dest)
        except Exception as exc:  # ocean tiles simply don't exist
            print(f"  ! {name}: {exc}")
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sites", default="data/sites.json")
    ap.add_argument("--dem-dir", default="data/dem")
    ap.add_argument("--source", choices=["aster", "copernicus"], default="aster")
    ap.add_argument("--only", help="comma-separated site ids")
    args = ap.parse_args()

    sites = [x for x in json.load(open(args.sites)) if x["role"] != "moon"]
    if args.only:
        keep = set(args.only.split(","))
        sites = [x for x in sites if x["id"] in keep]

    if args.source == "aster":
        import earthaccess
        earthaccess.login()  # prompts once, or uses ~/.netrc

    for site in sites:
        out_dir = os.path.join(args.dem_dir, "earth", site["id"])
        os.makedirs(out_dir, exist_ok=True)
        print(f"{site['id']}:")
        files = (download_aster if args.source == "aster" else download_copernicus)(site, out_dir)
        print(f"  {len(files)} file(s) in {out_dir}")


if __name__ == "__main__":
    main()
