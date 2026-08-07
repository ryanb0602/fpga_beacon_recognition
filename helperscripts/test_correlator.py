import casperfpga
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from python.psuedo_gc import psuedo_gc 

def to_signed(val, bits):
    if val & (1 << (bits - 1)):
        val -= (1 << bits)
    return val

def unpack(arr):
    temp_arr = []
    ct = 0
    for i in arr:
        if ct % 4 != 0:
            temp_arr.append(i)
        ct += 1
    
    new_arr = [
        (a << 16) | (b << 8) | c
        for a, b, c in zip(temp_arr[0::3], temp_arr[1::3], temp_arr[2::3])
    ]

    return [to_signed(x, 24) for x in new_arr]

def read_re_values(fpga):
    values = fpga.read("Subsystem7_re_val_recorder_re_val", 1048576, 0)

    return unpack(values)

def read_i_values(fpga):
    values = fpga.read("Subsystem7_iq_recorder_i_samples", 16384, 0)

    return unpack(values)

def read_q_values(fpga):
    values = fpga.read("Subsystem7_iq_recorder_q_samples", 16384, 0)

    return unpack(values)

fpga = casperfpga.CasperFpga('192.168.20.60')
time.sleep(3)
if (not fpga.is_connected()):
    print("Did not connect to fpga")
    die = 5 / 0

upsamp_gc = np.array([item for item in psuedo_gc for _ in range(4)])

upsamp_gc = upsamp_gc + 0 * 1j

gc_fft_conj = np.conjugate(np.fft.fft(upsamp_gc, 4096))

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([])
ax.set_xlabel("index")
ax.set_ylabel("magnitude")


accum = np.zeros(4096)
a = 0
periods = 0

while(1):

    time.sleep(.1)
    fig.canvas.flush_events()

    iq_valid = fpga.read_int('Subsystem7_iq_recorder_iq_rdy')

    i = []
    q = []

    ifft = []

    if (iq_valid):
        i = read_i_values(fpga)
        q = read_q_values(fpga)

        fpga.write_int('Subsystem7_iq_recorder_iq_record', 1)
        fpga.write_int('Subsystem7_iq_recorder_iq_record', 0)

        iq = np.array(i) + 1j * np.array(q)
        fourier = np.fft.fft(iq)
        preifft = iq * gc_fft_conj

        ifft = np.fft.ifft(preifft)

        accum = accum + fourier #changed to look at fft

        a += 1
    
    if (a < periods): continue

    line.set_xdata(np.arange(len(accum)))
    line.set_ydata(accum)
    #line.set_ydata(i)
    ax.relim()
    ax.autoscale_view()

    fig.canvas.draw()
    fig.canvas.flush_events()

    a = 0
    accum = np.zeros(4096)

    time.sleep(.001)
