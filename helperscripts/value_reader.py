import casperfpga
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

line1, = ax1.plot([], [], color='blue', label='I')
line2, = ax1.plot([], [], color='orange', label='Q')
line3, = ax2.plot([], [], color='green', label='Re value')

ax1.legend(loc="upper right")
ax2.legend(loc="upper right")

is_paused = False

def on_key_press(event):
    global is_paused
    if event.key == ' ':
        is_paused = not is_paused
        if is_paused:
            print("Plot PAUSED. Press Spacebar to resume.")
        else:
            print("Plot RESUMED.")

fig.canvas.mpl_connect('key_press_event', on_key_press)

plt.ion()

plt.show()

while(1):

    time.sleep(.1)
    fig.canvas.flush_events()
    if is_paused: continue

    iq_valid = fpga.read_int('Subsystem7_iq_recorder_iq_rdy')
    re_valid = fpga.read_int('Subsystem7_re_val_recorder_re_rdy')

    new_iq = False
    new_re = False

    i = []
    q = []
    re = []

    if (iq_valid):
        i = read_i_values(fpga)
        q = read_q_values(fpga)

        fpga.write_int('Subsystem7_iq_recorder_iq_record', 1)
        fpga.write_int('Subsystem7_iq_recorder_iq_record', 0)

        new_iq = True
    
    if (re_valid):
        re = read_re_values(fpga)

        fpga.write_int('Subsystem7_re_val_recorder_re_record', 1)
        fpga.write_int('Subsystem7_re_val_recorder_re_record', 0)

        new_re = True
    
    if (new_iq and new_re):

        # 1. Generate x-axes that span the exact same range (e.g., 0 to 1) 
        # so the subplots align, regardless of how long the arrays are
        x_iq = np.linspace(0, 1, len(i))
        x_re = np.linspace(0, 1, len(re))

        # 2. Update the plot lines with the newly read data
        line1.set_data(x_iq, i)
        line2.set_data(x_iq, q)
        line3.set_data(x_re, re)

        # 3. Automatically adjust the Y-axis limits to fit the new data spikes
        ax1.relim()
        ax1.autoscale_view()
        ax2.relim()
        ax2.autoscale_view()

        # 4. Redraw the figure and process GUI events so the window doesn't freeze
        fig.canvas.draw()

        new_iq = False
        new_re = False


