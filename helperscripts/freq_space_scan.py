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

    noise_space = []
    peak_space = []

    for i in range(21):
        time.sleep(.1)

        fpga.write_int('Subsystem7_freq_shift_index', i)

        peak_val = fpga.read_int('out_peak_val')
        mean_val = fpga.read_int('out_noise_mean')

        #print("Freq increment: ", i)
        noise_space.append(mean_val)
        peak_space.append(peak_val)

    print("Peak space:", peak_space)
    print("Noise space:", noise_space)
