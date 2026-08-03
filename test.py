import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# from new_taps import taps1, taps2, taps3

mat_data = scipy.io.loadmat("for_corr.mat")

# Replace this array with your own FIR filter taps
taps1 = mat_data["a_1"].flatten()
taps2 = mat_data["b0_2"].flatten()
taps3 = mat_data["b0_3"].flatten()

# ==========================================
# 1. Define System Parameters
# ==========================================
fs_in = 1.966e9  # Stage 1 Input Rate: 1.966 GHz
D1 = 8  # Decimation 1: 1966 MHz -> 245.76 MHz
D2 = 10  # Decimation 2: 245.76 MHz -> 24.576 MHz
D3 = 6  # Decimation 3: 24.576 MHz -> 2.4576 MHz (Assumed)

# Replace these 3 lines with your actual taps from scipy.io.loadmat
# e.g., taps1 = mat_data["a_1"].flatten()
# Here we generate placeholder taps with correct anti-aliasing cutoffs
taps1 = signal.firwin(127, 110e6, fs=fs_in)  # Cutoff safely < 122.88 MHz
taps2 = signal.firwin(127, 11e6, fs=fs_in / D1)  # Cutoff safely < 12.288 MHz
taps3 = signal.firwin(127, 1e6, fs=fs_in / (D1 * D2))  # Cutoff safely < 1.2288 MHz

# ==========================================
# 2. Zero-Stuffing (Noble Identities)
# ==========================================
# Move Stage 2 to the input rate by inserting (D1 - 1) zeros between each tap
taps2_up = np.zeros(len(taps2) * D1)
taps2_up[::D1] = taps2

# Move Stage 3 to the input rate by inserting (D1 * D2 - 1) zeros between each tap
D_total_3 = D1 * D2
taps3_up = np.zeros(len(taps3) * D_total_3)
taps3_up[::D_total_3] = taps3

# ==========================================
# 3. Convolve into a Composite Filter
# ==========================================
# Convolving in the time domain is equivalent to multiplying in the frequency domain
composite_taps = np.convolve(taps1, taps2_up)
composite_taps = np.convolve(composite_taps, taps3_up)

# ==========================================
# 4. Calculate & Plot Frequency Response
# ==========================================
# Calculate response at the highest sample rate
w, h = signal.freqz(composite_taps, worN=16000, fs=fs_in)
magnitude = 20 * np.log10(np.abs(h) + 1e-12)  # 1e-12 prevents log(0) warnings

plt.figure(figsize=(12, 6))
plt.plot(w, magnitude, color="purple", linewidth=1.5)

plt.title("Composite Frequency Response of 3-Stage Decimator", fontsize=14)
plt.ylabel("Magnitude (dB)", fontsize=12)
plt.xlabel("Frequency (Hz)", fontsize=12)
plt.grid(True, which="both", ls="-", alpha=0.5)

# Limit the plot to the first Nyquist zone of the input, and set a practical dB floor
plt.xlim(0, fs_in / 2)
plt.ylim(-170, 10)

plt.tight_layout()
plt.show()
