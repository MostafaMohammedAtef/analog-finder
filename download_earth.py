"""Shared constants. Everyone imports these; nobody changes them after kickoff (H1)."""
import numpy as np

WINDOW_M = 10_000          # side of every analysis window, metres
GRID_M = 30                # every DEM (Earth and Moon) is resampled to this pixel size
N_PIX = WINDOW_M // GRID_M # 333 pixels per side

# Slope histogram: 0-45 degrees in 1-degree bins; anything steeper goes in the last bin
SLOPE_BINS = np.arange(0, 46, 1.0)
# Roughness histogram: 0-20 m in 1 m bins; anything rougher goes in the last bin
ROUGH_BINS = np.arange(0, 21, 1.0)
ROUGH_WIN = 5              # roughness = std of elevation in a 5 x 5 pixel (150 m) window

# Low-sun band used by the sun lane (Member 2)
LOW_SUN_MIN_DEG = 0.0
LOW_SUN_MAX_DEG = 5.0

# Default weights for the overall score (the app lets users change them)
WEIGHTS = {"slope": 1.0, "roughness": 1.0, "low_sun": 1.0}
