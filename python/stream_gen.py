import numpy as np
import asyncio
import matplotlib.pyplot as plt
import scipy.signal as signal

from psuedo_gc import psuedo_gc

class stream_generator:
    def __init__(self, gnss_string, gnss_fc, gnss_transmission_speed, wifi_fc, stream_sample_rate, relative_amplitude, noise=0, chunk_duration_s=0.005):
        
        self.chunk_duration_s = chunk_duration_s

        # Generate the wifi qam64 table
        self.qam64_levels = [-7, -5, -3, -1, 1, 3, 5, 7]
        self.qam64_choices = np.array([complex(i, q) for i in self.qam64_levels for q in self.qam64_levels])

        # Split gnss bytes into 2-bit segments for symbols, stored as a NumPy array for fast indexing
        self.gnss_trans_bytes = gnss_string.encode()
        self.gnss_bit_segments = np.array([(b >> s) & 0x03 for b in self.gnss_trans_bytes for s in (6, 4, 2, 0)])
        self.gnss_symbol_rate = gnss_transmission_speed / 2

        self.gnss_fc = gnss_fc

        self.wifi_channels = 64
        self.wifi_symbols_per_s = 250000
        self.wifi_bandwidth_per_channel = 20e6 / self.wifi_channels

        self.wifi_fc = wifi_fc
        self.sample_rate = stream_sample_rate
        
        # Pre-calculate GNSS I/Q mapping based on bit segments (0x0, 0x1, 0x2, 0x3)
        self.gnss_I_map = np.array([1, 0, -1, 0])
        self.gnss_Q_map = np.array([0, -1, 0, 1])

        # Pre-allocate wifi channel indices and frequencies
        self.wifi_i_indices = np.arange(1, self.wifi_channels + 1)
        self.wifi_channel_freqs = self.wifi_bandwidth_per_channel * self.wifi_i_indices

        self.chipping_rate = 1.023e6
        self.psuedo_gold_code = np.array(psuedo_gc)

        #store the desired relative_amplitude
        self.relative_amplitude_db = relative_amplitude

        #calculate relative scaling factors to adhere to set parameter
        calib_samples = int(self.sample_rate * 0.01) 
        calib_time = np.arange(calib_samples) / self.sample_rate
        
        gnss_calib = self.GNSS_signal(calib_time)
        wifi_calib = self.psuedo_wifi_noise(calib_time)
        
        gnss_base_power = np.mean(gnss_calib**2)
        wifi_base_power = np.mean(wifi_calib**2)

        # 1. Normalize GNSS to a baseline power of 1.0 (0 dB reference)
        self.gnss_scale = 1.0 / np.sqrt(gnss_base_power)

        # 2. Scale WiFi to match the relative dB parameter
        # Power ratio = 10^(dB/10), so Amplitude multiplier = sqrt(Power ratio)
        desired_wifi_power = 10 ** (self.relative_amplitude_db / 10)
        self.wifi_scale = np.sqrt(desired_wifi_power / wifi_base_power)

        #noise generated relative to gnss_scale
        self.desired_noise_power = 10 ** (-noise / 10)

    def GNSS_signal(self, time_array):
        # 1. Calculate symbol index for the entire time array at once
        symbols_transmitted = time_array * self.gnss_symbol_rate
        symbol_indices = (symbols_transmitted.astype(int)) % len(self.gnss_bit_segments)

        # 2. Map current bits to I and Q values using advanced indexing
        current_bits = self.gnss_bit_segments[symbol_indices]
        I_vals = self.gnss_I_map[current_bits]
        Q_vals = self.gnss_Q_map[current_bits]

        #mix in our psuedo gold code
        chips_transmitted = time_array * self.chipping_rate
        chip_indices = (chips_transmitted.astype(int)) % len(self.psuedo_gold_code)

        current_chips = self.psuedo_gold_code[chip_indices]

        I_vals_chipped = I_vals * current_chips
        Q_vals_chipped = Q_vals * current_chips

        # 3. Calculate the carrier phase array
        omega_t = self.gnss_fc * np.pi * 2 * time_array

        # 4. Return I/Q modulation for the whole chunk
        return I_vals_chipped * np.cos(omega_t) - Q_vals_chipped * np.sin(omega_t)

    def psuedo_wifi_noise(self, time_array):
        # 1. Determine which WiFi symbols fall into this time chunk
        symbol_nums = np.floor(self.wifi_symbols_per_s * time_array).astype(int)
        
        # 2. Find unique symbols to avoid re-seeding the RNG unnecessarily
        unique_symbols, inverse_indices = np.unique(symbol_nums, return_inverse=True)

        # 3. Generate QAM64 IQ arrays only for the unique symbols in this chunk
        iq_arrays = np.zeros((len(unique_symbols), self.wifi_channels), dtype=complex)
        for idx, sym in enumerate(unique_symbols):
            rng = np.random.default_rng(seed=int(sym))
            iq_arrays[idx] = rng.choice(self.qam64_choices, self.wifi_channels)

        # 4. Map the generated symbols back to the sample level
        # iq_per_sample shape: (len(time_array), 64 channels)
        iq_per_sample = iq_arrays[inverse_indices]
        i_val = iq_per_sample.real
        q_val = iq_per_sample.imag

        # 5. Broadcast frequencies against time to create an omega matrix
        # time_array shape: (N, 1), wifi_channel_freqs shape: (1, 64) -> omega shape: (N, 64)
        omega = 2 * np.pi * self.wifi_channel_freqs[np.newaxis, :] * time_array[:, np.newaxis]

        # 6. Perform the I/Q calculation and sum across the 64 channels simultaneously
        baseband_signal = np.sum(i_val * np.cos(omega) - q_val * np.sin(omega), axis=1)

        # 7. Modulate with the final carrier frequency
        carrier = np.cos(2 * np.pi * self.wifi_fc * time_array)
        
        return baseband_signal * carrier

    def signal_stream(self):
        samples_per_chunk = int(self.sample_rate * self.chunk_duration_s)
        current_time = 0.0 

        while True:
            # Generate the time array for the whole chunk at once
            time_array = np.arange(0, samples_per_chunk) / self.sample_rate + current_time

            # Bulk generate signals
            gnss_chunk = self.GNSS_signal(time_array)
            wifi_chunk = self.psuedo_wifi_noise(time_array)
            noise = np.random.normal(0, np.sqrt(self.desired_noise_power), samples_per_chunk)

            signal_out = self.gnss_scale * gnss_chunk + self.wifi_scale * wifi_chunk + noise
            #signal_out = gnss_chunk
            current_time += self.chunk_duration_s

            yield signal_out


if __name__ == "__main__":
    # 1. Initialize the generator with sample parameters
    gen = stream_generator(
        gnss_string="TEST_STRING",
        gnss_fc=2.046e6,                   # GNSS at 2x chip rate
        gnss_transmission_speed=50,
        wifi_fc=3e6,                   # WiFi at 5 MHz
        stream_sample_rate=10e6,       # 20 MHz sample rate
        chunk_duration_s=0.005,         # 5ms chunks
        noise=40,
        relative_amplitude=-100
    )

    # 2. Start the generator stream
    stream = gen.signal_stream()

    # 3. Collect and concatenate multiple chunks for a better spectrogram (e.g., 10 chunks = 50ms)
    print("Generating signal data in bulk...")
    num_chunks = 50
    signal_data = np.concatenate([next(stream) for _ in range(num_chunks)])

    # 4. Generate the plots
    print("Rendering plots...")
    plt.figure(figsize=(12, 8))

    # --- TOP PLOT: Time Domain ---
    plt.subplot(2, 1, 1)
    # Generate a time array for the concatenated data
    t = np.arange(len(signal_data)) / gen.sample_rate
    # Plot only the first 1000 samples so the waveforms are actually visible
    plt.plot(t[:1000], signal_data[:1000], color='C0')
    plt.title("Baseband Signal - Time Domain (First 1000 samples)")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)

    # --- BOTTOM PLOT: Spectrogram ---
    plt.subplot(2, 1, 2)
    # Calculate the spectrogram using scipy.signal
    f, t_spec, Sxx = signal.spectrogram(
        signal_data, 
        fs=gen.sample_rate, 
        nperseg=256, 
        noverlap=128,
        window='hann'
    )
    
    # Plot using pcolormesh (converted to dB scale for better visibility)
    plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud', cmap='viridis')
    plt.title("Signal Spectrogram")
    plt.ylabel("Frequency [Hz]")
    plt.xlabel("Time [s]")
    
    plt.ylim(0, 2.046e6)

    # Add a colorbar to indicate power intensity
    cbar = plt.colorbar()
    cbar.set_label('Power Spectral Density [dB]')

    # Clean up layout and display
    plt.tight_layout()
    plt.show()
