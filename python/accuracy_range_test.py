from fft_correlator import fft_correlator
from stream_gen import stream_generator

import numpy as np
import matplotlib.pyplot as plt
import random
import csv
from datetime import datetime

from psuedo_gc import psuedo_gc
from test_plotter import plot_3d_correlator_map

gnss_fc = 2.046e6
sample_rate = 10e6

snr_values = list(range(-50, 51, 10))
wifi_values = list(range(-100, 51, 10))

phase_shift_range = [0, 9999]
doppler_shift_range = [-1000, 1000]

tests_per_value = 10

csv_header = ["snr", "wifi_db", "exp_phase_shift", "exp_doppler_shift", "found_phase_shift", "found_doppler_shift"]

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"data/simulation_results_{timestamp}.csv"

with open(filename, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(csv_header)

    for snr in snr_values:
        for wifi_db in wifi_values:
            for test in range(tests_per_value):

                phase_shift = random.randint(phase_shift_range[0], phase_shift_range[1])
                doppler_shift = random.randint(doppler_shift_range[0], doppler_shift_range[1])

                gen = stream_generator(
                    gnss_string="TEST_STRING",
                    gnss_fc=gnss_fc + doppler_shift,                   # GNSS at 2x chip rate
                    gnss_transmission_speed=50,
                    wifi_fc=3e6,                   # WiFi about 1Mhz above gnss
                    stream_sample_rate=sample_rate,       # 10 MHz sample rate
                    chunk_duration_s=0.0004096,
                    noise=snr,
                    relative_amplitude=wifi_db,
                    phase_offset_samples=phase_shift 
                )

                fc = fft_correlator(gnss_fc, sample_rate, 1000, psuedo_gc)

                data_yielder = gen.signal_stream()

                corr_result = None
                data_list = []

                while True:
                    data = next(data_yielder)
                    cycle_complete = fc.load_and_sweep(data, gnss_fc)
                    if cycle_complete:
                        best_freq, best_phase = fc.get_results()
                        print(f"Peak found at Freq Offset: {best_freq}, Phase: {best_phase}")

                        writer.writerow([
                            snr,
                            wifi_db,
                            phase_shift,
                            doppler_shift,
                            best_phase,
                            best_freq
                            ]) 

                        break
