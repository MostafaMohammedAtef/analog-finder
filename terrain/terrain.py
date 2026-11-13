"""Terrain lane: slope + roughness histograms for every site, scored against the Moon and Mars.

Reads   data/sites.json, data/dem/earth/<id>/*dem*.tif, data/dem/<moon or mars dem path>
Writes  out/terrain.json   (shape agreed in CONTRACTS.md)

Every DEM is cut to a 10 x 10 km window and resampled to 30 m:
  Earth -> local UTM zone, bilinear;  Moon -> its own polar stereographic grid, averaged;
  Mars  -> local Transverse Mercator around the window centre, averaged.

Usage:
  python terrain.py                    # all sites
  python terrain.py --only svalbard    # one Earth site (+ the Moon and Mars references, always)
"""
import argparse
import glob
import json
import os
import warnings

import numpy as np
import rasterio
from pyproj import CRS, Transformer
from rasterio.merge import merge
from rasterio.transform import from_origin
from rasterio.warp import Resampling, reproject
from scipy.ndimage import uniform_filter

from constants import GRID_M, N_PIX, ROUGH_BINS, ROUGH_WIN, SLOPE_BINS

warnings.filterwarnings("ignore", category=RuntimeWarning)


# ---------- loading one 10 x 10 km window, 30 m grid ----------

def utm_crs(lat, lon):
    zone = int((lon + 180) // 6) + 1
    return CRS.from_epsg((32600 if lat >= 0 else 32700) + zone)


def earth_window(site, dem_dir):
    files = [f for f in glob.glob(os.path.join(dem_dir, "earth", site["id"], "*.tif"))
             if "dem" in os.path.basename(f).lower()]      # skips ASTER *_num.tif
    if not files:
        raise FileNotFoundError(f"no DEM tiles in {dem_dir}/earth/{site['id']}/")
    srcs = [rasterio.open(f) for f in files]
    nodata = srcs[0].nodata if srcs[0].nodata is not None else -9999
    mosaic, src_transform = merge(srcs, nodata=nodata)
    src_crs = srcs[0].crs
    for s in srcs:
        s.close()

    dst_crs = utm_crs(site["lat"], site["lon"])
    x, y = Transformer.from_crs("EPSG:4326", dst_crs, always_xy=True).transform(site["lon"], site["lat"])
    half = N_PIX * GRID_M / 2
    dst_transform = from_origin(x - half, y + half, GRID_M, GRID_M)
    z = np.full((N_PIX, N_PIX), np.nan, dtype="float64")
    reproject(mosaic[0].astype("float64"), z,
              src_transform=src_transform, src_crs=src_crs, src_nodata=nodata,
              dst_transform=dst_transform, dst_crs=dst_crs, dst_nodata=np.nan,
              resampling=Resampling.bilinear)
    return z


def planet_window_latlon(site, dem_dir):
    """Moon/Mars window centred on site lat/lon, cut on a local Transverse Mercator grid.

    A local projection keeps metres true in every direction, so slopes are not distorted by the
    file's own map projection (Mars mosaics are equirectangular, which stretches east-west)."""
    from pyproj.crs import ProjectedCRS
    from pyproj.crs.coordinate_operation import TransverseMercatorConversion
    from rasterio.crs import CRS as RioCRS

    path = os.path.join(dem_dir, site["dem"])
    with rasterio.open(path) as src:
        src_crs = CRS.from_user_input(src.crs.to_wkt())
        geo = src_crs.geodetic_crs
        local = ProjectedCRS(
            conversion=TransverseMercatorConversion(
                latitude_natural_origin=site["lat"], longitude_natural_origin=site["lon"],
                false_easting=0, false_northing=0, scale_factor_natural_origin=1.0),
            geodetic_crs=geo)
        n = N_PIX
        half = n * GRID_M / 2
        dst_transform = from_origin(-half, half, GRID_M, GRID_M)
        z = np.full((n, n), np.nan, dtype="float64")
        src_res = max(abs(src.res[0]), abs(src.res[1]))
        reproject(rasterio.band(src, 1), z,
                  src_transform=src.transform, src_crs=src.crs, src_nodata=src.nodata,
                  dst_transform=dst_transform, dst_crs=RioCRS.from_wkt(local.to_wkt()),
                  dst_nodata=np.nan,
                  resampling=Resampling.average if src_res < GRID_M else Resampling.bilinear)
    return z


def planet_window(site, dem_dir):
    """Reference window on the Moon or Mars. Uses lat/lon if given, else x/y or the file centre."""
    if "lat" in site and "lon" in site:
        return planet_window_latlon(site, dem_dir)
    return moon_window(site, dem_dir)


def moon_window(site, dem_dir):
    path = os.path.join(dem_dir, site["dem"])
    with rasterio.open(path) as src:
        b = src.bounds
        cx = site.get("x", (b.left + b.right) / 2)
        cy = site.get("y", (b.bottom + b.top) / 2)
        # Use the full 10 km if the file is big enough, otherwise the largest square that fits
        side = min(N_PIX * GRID_M, b.right - b.left, b.top - b.bottom)
        n = int(side // GRID_M)
        half = n * GRID_M / 2
        dst_transform = from_origin(cx - half, cy + half, GRID_M, GRID_M)
        z = np.full((n, n), np.nan, dtype="float64")
        reproject(rasterio.band(src, 1), z,
                  src_transform=src.transform, src_crs=src.crs, src_nodata=src.nodata,
                  dst_transform=dst_transform, dst_crs=src.crs, dst_nodata=np.nan,
                  resampling=Resampling.average)        # 5 m -> 30 m
    return z


# ---------- metrics ----------

def slope_deg(z):
    gy, gx = np.gradient(z, GRID_M)
    return np.degrees(np.arctan(np.hypot(gx, gy)))


def roughness_m(z):
    """Std of elevation in a ROUGH_WIN x ROUGH_WIN window; NaN where the window has gaps."""
    valid = np.isfinite(z)
    zf = np.where(valid, z - np.nanmean(z), 0.0)        # centre first to avoid precision loss
    w = uniform_filter(valid.astype("float64"), ROUGH_WIN, mode="constant")
    m = uniform_filter(zf, ROUGH_WIN, mode="constant")
    m2 = uniform_filter(zf * zf, ROUGH_WIN, mode="constant")
    with np.errstate(invalid="ignore", divide="ignore"):
        r = np.sqrt(np.clip(m2 / w - (m / w) ** 2, 0, None))
    r[w < 0.999] = np.nan
    return r


def norm_hist(values, bins):
    v = values[np.isfinite(values)]
    v = np.clip(v, bins[0], bins[-1] - 1e-9)             # overflow goes in the last bin
    h, _ = np.histogram(v, bins=bins)
    return (h / h.sum()) if h.sum() else np.zeros(len(bins) - 1)


def intersection(p, q):
    """Histogram intersection: 0 = no overlap, 1 = identical distributions."""
    return float(np.minimum(p, q).sum())


def describe(z):
    s, r = slope_deg(z), roughness_m(z)
    return {
        "slope_hist": norm_hist(s, SLOPE_BINS),
        "rough_hist": norm_hist(r, ROUGH_BINS),
        "slope_p50_deg": float(np.nanpercentile(s, 50)),
        "slope_p90_deg": float(np.nanpercentile(s, 90)),
        "rough_p50_m": float(np.nanpercentile(r, 50)),
        "relief_m": float(np.nanmax(z) - np.nanmin(z)),
        "valid_fraction": float(np.isfinite(z).mean()),
        "window_km": round(z.shape[0] * GRID_M / 1000, 2),
    }


def r3(x):
    return None if x is None else round(float(x), 3)


def to_json(d, slope_sim, rough_sim, mars_slope_sim=None, mars_rough_sim=None):
    return {
        "slope_hist": [r3(v) for v in d["slope_hist"]],
        "rough_hist": [r3(v) for v in d["rough_hist"]],
        "slope_similarity": r3(slope_sim),          # vs the Moon reference
        "roughness_similarity": r3(rough_sim),      # vs the Moon reference
        "mars_slope_similarity": r3(mars_slope_sim),
        "mars_roughness_similarity": r3(mars_rough_sim),
        "slope_p50_deg": r3(d["slope_p50_deg"]),
        "slope_p90_deg": r3(d["slope_p90_deg"]),
        "rough_p50_m": r3(d["rough_p50_m"]),
        "relief_m": r3(d["relief_m"]),
        "valid_fraction": r3(d["valid_fraction"]),
        "window_km": d["window_km"],
    }


def null_entry():
    keys = ["slope_hist", "rough_hist", "slope_similarity", "roughness_similarity",
            "mars_slope_similarity", "mars_roughness_similarity", "slope_p50_deg", "slope_p90_deg", "rough_p50_m", "relief_m",
            "valid_fraction", "window_km"]
    return {k: None for k in keys}


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sites", default="data/sites.json")
    ap.add_argument("--dem-dir", default="data/dem")
    ap.add_argument("--out", default="out/terrain.json")
    ap.add_argument("--only", help="comma-separated Earth site ids")
    args = ap.parse_args()

    sites = json.load(open(args.sites))
    planets = ("moon", "mars")
    earths = [s for s in sites if s["role"] not in planets]
    if args.only:
        keep = set(args.only.split(","))
        earths = [s for s in earths if s["id"] in keep]

    # Reference for each world = average of its windows' histograms
    desc = {p: {} for p in planets}
    for p in planets:
        for m in [s for s in sites if s["role"] == p]:
            try:
                d = describe(planet_window(m, args.dem_dir))
                desc[p][m["id"]] = d
                flag = "  (low coverage!)" if d["valid_fraction"] < 0.9 else ""
                print(f"{p:5s} {m['id']:24s} ok ({d['window_km']} km window, "
                      f"p90 slope {d['slope_p90_deg']:.1f} deg){flag}")
            except Exception as exc:
                print(f"{p:5s} {m['id']:24s} FAILED: {exc}")
    if not desc["moon"]:
        raise SystemExit("No Moon DEM loaded - download the LOLA site files first (see README).")
    if not desc["mars"]:
        print("mars  (no Mars DEM loaded - Mars scores will be null; see README_TERRAIN.md)")

    ref = {p: (np.mean([d["slope_hist"] for d in desc[p].values()], axis=0),
               np.mean([d["rough_hist"] for d in desc[p].values()], axis=0))
           for p in planets if desc[p]}

    def sims(d, p):
        if p not in ref:
            return None, None
        return intersection(d["slope_hist"], ref[p][0]), intersection(d["rough_hist"], ref[p][1])

    out = {}
    # Each reference window vs the OTHER window(s) of the same world: how different two real
    # spots on that world are from each other. Also scored against the other world, for interest.
    for p in planets:
        for mid, d in desc[p].items():
            others = [o for k, o in desc[p].items() if k != mid]
            if others:
                own = (intersection(d["slope_hist"], np.mean([o["slope_hist"] for o in others], axis=0)),
                       intersection(d["rough_hist"], np.mean([o["rough_hist"] for o in others], axis=0)))
            else:
                own = (None, None)
            if p == "moon":
                out[mid] = to_json(d, *own, *sims(d, "mars"))
            else:
                out[mid] = to_json(d, *sims(d, "moon"), *own)

    def f(x):
        return " -- " if x is None else f"{x:.2f}"

    for s in earths:
        try:
            d = describe(earth_window(s, args.dem_dir))
            ms, mr = sims(d, "moon")
            xs, xr = sims(d, "mars")
            out[s["id"]] = to_json(d, ms, mr, xs, xr)
            flag = "  (low coverage!)" if d["valid_fraction"] < 0.9 else ""
            print(f"earth {s['id']:24s} MOON slope {f(ms)} rough {f(mr)} | "
                  f"MARS slope {f(xs)} rough {f(xr)} | p90 slope {d['slope_p90_deg']:.1f} deg{flag}")
        except Exception as exc:
            out[s["id"]] = null_entry()
            print(f"earth {s['id']:24s} SKIPPED: {exc}")

    # Keep earlier results for sites not run this time (so --only doesn't wipe others)
    if args.only and os.path.exists(args.out):
        old = json.load(open(args.out))
        for k, v in old.items():
            out.setdefault(k, v)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    json.dump(out, open(args.out, "w"), indent=1)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
