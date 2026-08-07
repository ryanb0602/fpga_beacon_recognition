
import casperfpga
import numpy as np
import time
import matplotlib.pyplot as plt

fpga = casperfpga.CasperFpga('192.168.20.60')
time.sleep(3)
if (not fpga.is_connected()):
    print("Did not connect to fpga")
    die = 5 / 0

while(1):
    adc = []
    for i in range(200):
        adc.append(fpga.read_int("adc_real_stream"))
    plt.plot(adc)
    plt.show()
