import casperfpga
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fpga = casperfpga.CasperFpga('192.168.20.60')
time.sleep(3)
if (not fpga.is_connected()):
    print("Did not connect to fpga")
    die = 5 / 0

while(1):

    time.sleep(.1)

    peak_val = fpga.read_int('out_peak_val')
    mean_val = fpga.read_int('out_noise_mean')

    if (mean_val == 0):
        print("Noise val: 0, peak: ", peak_val)
    else:
        print("SNR: ", peak_val / mean_val)
