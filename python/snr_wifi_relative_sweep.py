from fft_correlator import fft_correlator
from stream_gen import stream_generator

import numpy as np
import matplotlib.pyplot as plt

from psuedo_gc import psuedo_gc
from test_plotter import plot_3d_correlator_map

gnss_fc = 2.046e6
sample_rate = 10e6

snr_values = list(range(-30, 31, 20))
wifi_values = list(range(-100, 51, 25))

for snr_val in snr_values:
    for wifi_val in wifi_values:

        gen = stream_generator(
            gnss_string="TEST_STRING",
            gnss_fc=gnss_fc,                   # GNSS at 2x chip rate
            gnss_transmission_speed=50,
            wifi_fc=3e6,                   # WiFi about 1Mhz above gnss
            stream_sample_rate=sample_rate,       # 10 MHz sample rate
            chunk_duration_s=0.0004096,
            noise=snr_val,
            relative_amplitude=wifi_val
        )

        fc = fft_correlator(gnss_fc, sample_rate, 1000, psuedo_gc, 50)

        data_yielder = gen.signal_stream()

        corr_result = None
        data_list = []

        while True:
            data = next(data_yielder)
            corr_result = fc.load_and_sweep(data, gnss_fc)
            if corr_result is not None:
                data_list.extend(corr_result)
                break
        plot_3d_correlator_map(data_list, str(snr_val) + "snr_" + str(wifi_val) + "wifi")
