import numpy as np
import asyncio
import matplotlib.pyplot as plt
import scipy.signal as signal
import scipy.fft as fft
from collections import deque

from psuedo_gc import psuedo_gc

class fft_correlator:
    def __init__(self, target_carry_freq, samp_rate, scan_range, gold_code, scan_step = 100):
        self.target_carry_freq = target_carry_freq
        self.scan_range = scan_range
        self.psuedo_gc = np.array(gold_code)

        self.sample_rate = samp_rate

        self.chipping_rate = 1.023e6

        self.samples_per_code = int((len(self.psuedo_gc) / self.chipping_rate) * self.sample_rate)

        self.buffer_size = self.samples_per_code * 2

        time_array = np.arange(self.samples_per_code) / self.sample_rate
        chip_indices = (time_array * self.chipping_rate).astype(int) % len(self.psuedo_gc)
        time_domain_gc = self.psuedo_gc[chip_indices]
        padded_td_gc = np.concatenate((time_domain_gc, np.zeros(self.buffer_size - len(time_domain_gc))))

        self.gc_conjugate = np.conj(fft.fft(padded_td_gc))


        self.scan_freqs = np.arange(-scan_range, scan_range, scan_step)

        self.data_buffer = [deque(maxlen=self.buffer_size) for _ in range(len(self.scan_freqs))]

        self.samples_processed = []
        for i in range(len(self.scan_freqs)):
            self.samples_processed.append(0)

        self.correlator_results = []

    def load_and_sweep(self, stream, center_freq):

        data_collected = []

        for i in range(len(self.scan_freqs)):

            self.load_stream(stream, center_freq + self.scan_freqs[i], i)
            corr_output = self.correlate(i)
            
            if corr_output is not None:
                data_collected.append((self.scan_freqs[i], corr_output))

        if (len(data_collected) > 0):
            self.correlator_results = data_collected
            return data_collected
        
        return None

    def load_stream(self, stream, center_freq, buffer_index):
        raw_voltage = np.array(stream)

        time_array = np.arange(0, len(raw_voltage)) / self.sample_rate
        if (self.samples_processed[buffer_index] > 0):
            time_array += self.samples_processed[buffer_index] / self.sample_rate
        omega_t = center_freq * np.pi * 2 * time_array

        I_vals = raw_voltage * np.cos(omega_t)
        Q_vals = raw_voltage * np.sin(omega_t)

        self.data_buffer[buffer_index].extend(I_vals - 1j * Q_vals)
        self.samples_processed[buffer_index] += len(raw_voltage)

    def correlate(self, buffer_index):
        iq_arr = np.array(self.data_buffer[buffer_index])

        if len(iq_arr) != self.buffer_size:
            return None
        iq_arr_fft = fft.fft(iq_arr)

        conj_array = self.gc_conjugate

        freq_prod = iq_arr_fft * conj_array
        #return freq_prod
        return fft.ifft(freq_prod)

    def get_results(self):
        processed_bins = []
        
        for bin in self.correlator_results:
            cut_to_one_phase = bin[1][:self.samples_per_code]
            magnitudes = np.abs(cut_to_one_phase)

            processed_bins.append((bin[0], magnitudes))

        current_max = 0
        current_max_tup = None

        for bin in processed_bins:
            max_index = np.argmax(bin[1])
            if bin[1][max_index] > current_max:
                current_max = bin[1][max_index]
                current_max_tup = (bin[0], max_index)

        print(current_max_tup)
