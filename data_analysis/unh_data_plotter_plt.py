import contextily as cx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyproj import Transformer
from scipy.interpolate import griddata
from scipy.spatial import cKDTree

# -------------------------------------------------------------
# 1. Load Data & Coordinate Transformation
# -------------------------------------------------------------
target_files = [
    "./unh_collection/fpga_data_20260805_135043.csv",
    "./unh_collection/fpga_data_20260805_151921.csv",
]

df = pd.concat((map(pd.read_csv, target_files)), ignore_index=True)

new_datetime = pd.to_datetime(df["time"], format="%Y%m%d_%H%M%S")
df["time"] = new_datetime
df = df.set_index("time")

to_projected = Transformer.from_crs(4326, 32619, always_xy=True)
to_wgs84 = Transformer.from_crs(32619, 4326, always_xy=True)

x, y = to_projected.transform(df["lon"].values, df["lat"].values)

df["x"] = x
df["y"] = y

df["x"] = df["x"].interpolate(method="time")
df["y"] = df["y"].interpolate(method="time")

lon, lat = to_wgs84.transform(df["x"].values, df["y"].values)
df["lon"] = lon
df["lat"] = lat

df = df.drop(columns=["x", "y"]).dropna()

# -------------------------------------------------------------
# 2. Bounding Box Pre-Filtering
# -------------------------------------------------------------
min_lat = 43.125691
max_lat = df["lat"].max()
min_lon = df["lon"].min()
max_lon = -70.92

# Filter dataframe within bounding box before gridding
df = df[df["lat"].between(min_lat, max_lat) & df["lon"].between(min_lon, max_lon)]

# -------------------------------------------------------------
# 3. Spatial Grid Averaging
# -------------------------------------------------------------
cell_distance = 20  # meters

lat_cell = cell_distance / 111132
long_cell = cell_distance / (111412 * np.cos(np.radians(43.134)))

lat_gridlines = np.arange(min_lat, max_lat, lat_cell)
long_gridlines = np.arange(min_lon, max_lon, long_cell)

output_vals = []

for i in range(len(lat_gridlines) - 1):
    for j in range(len(long_gridlines) - 1):
        lat_s, lat_e = lat_gridlines[i], lat_gridlines[i + 1]
        long_s, long_e = long_gridlines[j], long_gridlines[j + 1]

        target_range = df[
            df["lat"].between(lat_s, lat_e) & df["lon"].between(long_s, long_e)
        ]

        if not target_range.empty:
            avg_p = target_range["peak_val"].mean()
            avg_e = target_range["noise_mean"].mean()
        else:
            avg_p = np.nan
            avg_e = np.nan

        output_vals.append((lat_s, lat_e, long_s, long_e, avg_p, avg_e))

output_df = pd.DataFrame(
    output_vals,
    columns=[
        "lat_start",
        "lat_end",
        "lon_start",
        "lon_end",
        "avg_peak_val",
        "avg_noise_mean",
    ],
).dropna(subset=["avg_peak_val", "avg_noise_mean"])

# Calculate cell center coordinates & SNR (dB)
output_df["center_lat"] = (output_df["lat_start"] + output_df["lat_end"]) / 2
output_df["center_lon"] = (output_df["lon_start"] + output_df["lon_end"]) / 2
output_df["snr"] = 20 * np.log10(
    output_df["avg_peak_val"] / output_df["avg_noise_mean"]
)

plot_data = output_df.dropna(subset=["center_lat", "center_lon", "snr"])

# Shared Color Scale Limits
vmin_snr = plot_data["snr"].min()
vmax_snr = plot_data["snr"].max()

# Key Reference Point (Star)
star_lat, star_lon = 43.134, -70.932

vmin_snr = plot_data["snr"].min()
vmax_snr = plot_data["snr"].max()

# -------------------------------------------------------------
# Fix 2: High-Resolution Grid + Proximity Mask
# -------------------------------------------------------------
points = np.column_stack(
    (plot_data["center_lon"].values, plot_data["center_lat"].values)
)

# Mesh resolution
grid_lon = np.linspace(points[:, 0].min(), points[:, 0].max(), 350)
grid_lat = np.linspace(points[:, 1].min(), points[:, 1].max(), 350)
grid_lon_mesh, grid_lat_mesh = np.meshgrid(grid_lon, grid_lat)

# 1. Linear spatial interpolation (no wild cubic overshoots)
grid_snr = griddata(
    points,
    plot_data["snr"].values,
    (grid_lon_mesh, grid_lat_mesh),
    method="linear",
)

# 2. Mask out grid cells farther than ~50m from actual data points
# (0.0005 deg latitude/longitude is approx 50 meters)
max_distance_deg = 0.0005
tree = cKDTree(points)
grid_coords = np.column_stack((grid_lon_mesh.ravel(), grid_lat_mesh.ravel()))
distances, _ = tree.query(grid_coords)

mask = distances > max_distance_deg
grid_snr_masked = grid_snr.copy()
grid_snr_masked[mask.reshape(grid_lon_mesh.shape)] = np.nan

# -------------------------------------------------------------
# 3. Figure Rendering
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), sharex=True, sharey=True)
plt.rcParams.update({"font.size": 13, "font.family": "sans-serif"})

# --- LEFT PLOT: Discrete Points ---
sc = ax1.scatter(
    plot_data["center_lon"],
    plot_data["center_lat"],
    c=plot_data["snr"],
    cmap="viridis",
    vmin=vmin_snr,
    vmax=vmax_snr,
    s=35,
    alpha=0.9,
    edgecolors="none",
)
ax1.scatter(
    star_lon,
    star_lat,
    marker="*",
    color="gold",
    s=300,
    edgecolors="black",
    linewidth=1.2,
    zorder=5,
    label="Sensor Station",
)

ax1.set_title("Discrete SNR Measurements (dB)", fontsize=15, fontweight="bold")
ax1.set_xlabel("Longitude")
ax1.set_ylabel("Latitude")
ax1.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.9)

cbar1 = fig.colorbar(sc, ax=ax1, fraction=0.046, pad=0.04)
cbar1.set_label("SNR (dB)", fontsize=13, fontweight="bold")

# --- RIGHT PLOT: Masked Smooth Track Heatmap ---
cf = ax2.contourf(
    grid_lon_mesh,
    grid_lat_mesh,
    grid_snr_masked,
    levels=15,
    cmap="viridis",
    vmin=vmin_snr,
    vmax=vmax_snr,
    alpha=0.85,
)
ax2.scatter(
    star_lon,
    star_lat,
    marker="*",
    color="gold",
    s=300,
    edgecolors="black",
    linewidth=1.2,
    zorder=5,
)

ax2.set_title("Smooth Track SNR Surface (Masked)", fontsize=15, fontweight="bold")
ax2.set_xlabel("Longitude")

cbar2 = fig.colorbar(cf, ax=ax2, fraction=0.046, pad=0.04)
cbar2.set_label("SNR (dB)", fontsize=13, fontweight="bold")

# Add Basemaps
cx.add_basemap(ax1, crs="EPSG:4326", source=cx.providers.CartoDB.Positron)
cx.add_basemap(ax2, crs="EPSG:4326", source=cx.providers.CartoDB.Positron)

plt.tight_layout()

fig.savefig("spatial_snr_poster_fixed.png", dpi=300, bbox_inches="tight")
print("Saved clean spatial figure to spatial_snr_poster_fixed.png")
