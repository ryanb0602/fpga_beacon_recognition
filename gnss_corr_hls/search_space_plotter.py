import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def plot_gnss_search_space(csv_path="gnss_search_space.csv"):
    # Load search grid data
    df = pd.read_csv(csv_path)

    # Pivot into 2D Grid Matrix (Rows: Doppler Shift, Columns: Code Lag)
    grid = df.pivot(index="doppler_hz", columns="lag", values="magnitude")

    dopplers = grid.index.values
    lags = grid.columns.values
    magnitudes = grid.values

    # Locate peak in matrix
    max_idx = np.unravel_index(np.argmax(magnitudes, axis=None), magnitudes.shape)
    peak_doppler_idx, peak_lag_idx = max_idx
    peak_doppler = dopplers[peak_doppler_idx]
    peak_lag = lags[peak_lag_idx]
    peak_mag = magnitudes[max_idx]

    print(f"Acquisition Peak Details:")
    print(f"  Max Magnitude : {peak_mag:.6f}")
    print(f"  Doppler Shift : {peak_doppler:.1f} Hz")
    print(f"  Code Lag      : {peak_lag} samples")

    fig = plt.figure(figsize=(10, 8))

    # --- 3D Surface Only ---
    ax = fig.add_subplot(1, 1, 1, projection="3d")
    X, Y = np.meshgrid(lags, dopplers)

    # Render surface
    surf = ax.plot_surface(
        X,
        Y,
        magnitudes,
        cmap=cm.viridis,
        edgecolor="none",
        alpha=0.85,
        rstride=1,
        cstride=10,
    )
    cbar = fig.colorbar(surf, ax=ax, shrink=0.6, pad=0.1)
    cbar.set_label("Correlation Magnitude", fontsize=11)

    # Vertical red stem and top marker so the 1-sample spike stands out in 3D space
    ax.plot(
        [peak_lag, peak_lag],
        [peak_doppler, peak_doppler],
        [0, peak_mag],
        color="red",
        linewidth=2.5,
    )
    ax.scatter(
        peak_lag,
        peak_doppler,
        peak_mag,
        color="red",
        s=50,
        label=f"Peak = {peak_mag:.2f} ({peak_lag}, {peak_doppler:.0f} Hz)",
    )

    ax.set_title("3D Correlation Peak Surface", fontsize=14, fontweight="bold")
    ax.set_xlabel("Code Delay (samples)", fontsize=11)
    ax.set_ylabel("Doppler Shift (Hz)", fontsize=11)
    ax.set_zlabel("Correlation Magnitude", fontsize=11)
    ax.view_init(elev=25, azim=225)
    ax.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig("gnss_3d_search_space.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    plot_gnss_search_space()
