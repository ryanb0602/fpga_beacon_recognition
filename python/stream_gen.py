import numpy as np
import asyncio
import matplotlib.pyplot as plt


#This generates a stream of simulated GNSS and Wifi transmissions alongside each other (GNSS at baseband, WiFi slightly higher) to simulate a GNSS format beacon.

#Generates GNNS waveform at baseband with set bandwidth. Uses QPSK. Transmission speed in bps
def GNSS_signal(transmission_string, current_time_s, fc = 1000, transmission_speed = 50):

    #convert transmission string to bytes
    trans_bytes = transmission_string.encode();
   
    #convert byte array to 2 bit segments for transmission
    bit_segments = [(b >> s) & 0x03 for b in trans_bytes for s in (6, 4, 2, 0)]

    #what symbol should you be transmitting at current time
    symbol_rate = transmission_speed / 2
    symbols_transmitted = current_time_s * symbol_rate
    symbol_index = int(symbols_transmitted) % len(bit_segments)

    omega_t = fc * np.pi * 2 * current_time_s

    #I/Q modulation
    if (bit_segments[symbol_index] == 0x0):
        return np.cos(omega_t)
    elif (bit_segments[symbol_index] == 0x1):
        return np.sin(omega_t)
    elif (bit_segments[symbol_index] == 0x2):
        return -np.cos(omega_t)
    elif (bit_segments[symbol_index] == 0x3):
        return -np.sin(omega_t)

