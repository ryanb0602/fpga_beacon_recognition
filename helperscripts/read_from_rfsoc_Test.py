import casperfpga
import numpy as np
import time
import matplotlib.pyplot as plt

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

def read_i_values(fpga):
    values = fpga.read("i_output", 16384, 0)

    return unpack(values)

def read_q_values(fpga):
    values = fpga.read("q_output", 16384, 0)

    return unpack(values)


plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([])
ax.set_xlabel("index")
ax.set_ylabel("magnitude")

fpga = casperfpga.CasperFpga('192.168.20.60')
time.sleep(3)
if (not fpga.is_connected()):
    print("Did not connect to fpga")
    die = 5 / 0

accum = np.zeros(4096)
a = 0
periods = 0


while(1):

    vo = fpga.read_int("read_ready")

    if vo != 1: continue

    q = read_q_values(fpga)
    i = read_i_values(fpga)

    fpga.write_int("resume", 1)
    fpga.write_int("resume", 0)

    mag = np.hypot(np.array(i), np.array(q))

    accum = accum + mag


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
