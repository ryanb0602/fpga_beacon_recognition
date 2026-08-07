import numpy as np
import pandas as pd
from pyproj import Transformer
import contextily as cx
import matplotlib.pyplot as plt

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

df = df.drop(columns=["x", "y"])
df = df.dropna()

max_lat = max(df["lat"])
# min_lat = min(df["lat"])
min_lat = 43.125691

# max_lon = max(df["lon"])
max_lon = -70.92
min_lon = min(df["lon"])

cell_distance = 20  # meters

lat_cell = cell_distance / 111132
long_cell = cell_distance / (111412 * np.cos(np.radians(43.134)))

lat_gridlines = np.arange(min_lat, max_lat, lat_cell)
long_gridlines = np.arange(min_lon, max_lon, long_cell)

output_vals = []

for i in range(len(lat_gridlines) - 1):
    for j in range(len(long_gridlines) - 1):
        lat_s = lat_gridlines[i]
        lat_e = lat_gridlines[i + 1]

        long_s = long_gridlines[j]
        long_e = long_gridlines[j + 1]

        lat_range = df[df["lat"].between(lat_s, lat_e)]
        target_range = lat_range[lat_range["lon"].between(long_s, long_e)]

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
)


output_df = output_df.dropna(subset=["avg_peak_val", "avg_noise_mean"])
output_df["center_lat"] = (output_df["lat_start"] + output_df["lat_end"]) / 2
output_df["center_lon"] = (output_df["lon_start"] + output_df["lon_end"]) / 2

output_df["snr"] = 20 * np.log10(
    output_df["avg_peak_val"] / output_df["avg_noise_mean"]
)

plot_data = output_df.dropna(subset=["center_lat", "center_lon", "snr"])


star_lat, star_lon = 43.1336701, -70.9354358

fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
plt.rcParams.update({"font.size": 13, "font.family": "sans-serif"})

# vmin_snr = plot_data["snr"].min()
# vmax_snr = plot_data["snr"].max()

vmin_snr = np.percentile(plot_data["snr"], 2)
vmax_snr = np.percentile(plot_data["snr"], 98)

sc = ax.scatter(
    plot_data["center_lon"],
    plot_data["center_lat"],
    c=plot_data["snr"],
    cmap="turbo",
    vmin=vmin_snr,
    vmax=vmax_snr,
    s=45,
    alpha=0.9,
    edgecolors="none",
)

ax.scatter(
    star_lon,
    star_lat,
    marker="*",
    color="gold",
    s=350,
    edgecolors="black",
    linewidth=1.2,
    zorder=5,
    label="Beacon Location",
)

ax.set_title("Discrete Grid SNR (dB)", fontsize=16, fontweight="bold", pad=12)
ax.set_xlabel("Longitude", fontsize=13)
ax.set_ylabel("Latitude", fontsize=13)
ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)

cbar = fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("SNR (dB)", fontsize=13, fontweight="bold")

cx.add_basemap(ax, crs="EPSG:4326", source=cx.providers.CartoDB.Positron)

plt.tight_layout()

fig.savefig("spatial_snr_single_map_300dpi.png", dpi=300, bbox_inches="tight")
fig.savefig("spatial_snr_single_map.pdf", bbox_inches="tight")
print("Saved single map plot successfully!")
