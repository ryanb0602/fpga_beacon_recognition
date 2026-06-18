from fft_correlator import fft_correlator
from stream_gen import stream_generator

import numpy as np
import matplotlib.pyplot as plt

from psuedo_gc import psuedo_gc
from test_plotter import plot_3d_correlator_map

gnss_fc = 2.046e6
sample_rate = 10e6

gen = stream_generator(
    gnss_string="TEST_STRING",
    gnss_fc=gnss_fc,                   # GNSS at 2x chip rate
    gnss_transmission_speed=50,
    wifi_fc=3e6,                   # WiFi about 1Mhz above gnss
    stream_sample_rate=sample_rate,       # 10 MHz sample rate
    chunk_duration_s=10000 / sample_rate,
    noise=30,
    relative_amplitude=-100,
    phase_offset_samples=0 
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
