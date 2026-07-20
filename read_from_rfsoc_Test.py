import casperfpga
import numpy as np
import time
import matplotlib.pyplot as plt

def to_signed(val, bits):
    if val & (1 << (bits - 1)):
        val -= (1 << bits)
    return val

def fbp17(raw18):
    return to_signed(raw18, 18) / (1 << 17)

def unpack(bit_arr):
    cnt = 0
    valids_arr = []
    for i in range(len(bit_arr)):
        if cnt < 9:
            valids_arr.append(bit_arr[i])
        cnt += 1
        if cnt > 15:
            cnt = 0

    bits = int.from_bytes(bytes(valids_arr), 'big')
    nwords = len(valids_arr) * 8 // 18
    words = [(bits >> (i*18)) & 0x3FFFF for i in reversed(range(nwords))]
    
    return words

def read_i_values(fpga):
    segment_one = fpga.read("Subsystem1_shared_bram", 1024, 0)
    segment_two = fpga.read("Subsystem1_shared_bram1", 1024, 0)
    segment_three = fpga.read("Subsystem1_shared_bram2", 1024, 0)
    segment_four = fpga.read("Subsystem1_shared_bram3", 1024, 0)

    seg_a_unpacked = unpack(segment_one)
    seg_b_unpacked = unpack(segment_two)
    seg_c_unpacked = unpack(segment_three)
    seg_d_unpacked = unpack(segment_four)

    result = [x for group in zip(seg_a_unpacked, seg_b_unpacked, seg_c_unpacked, seg_d_unpacked) for x in group]
    
    return result

def read_q_values(fpga):
    segment_one = fpga.read("Subsystem2_shared_bram", 1024, 0)
    segment_two = fpga.read("Subsystem2_shared_bram1", 1024, 0)
    segment_three = fpga.read("Subsystem2_shared_bram2", 1024, 0)
    segment_four = fpga.read("Subsystem2_shared_bram3", 1024, 0)

    seg_a_unpacked = unpack(segment_one)
    seg_b_unpacked = unpack(segment_two)
    seg_c_unpacked = unpack(segment_three)
    seg_d_unpacked = unpack(segment_four)

    result = [x for group in zip(seg_a_unpacked, seg_b_unpacked, seg_c_unpacked, seg_d_unpacked) for x in group]
    
    return result


plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([])
ax.set_xlabel("index")
ax.set_ylabel("magnitude")

fpga = casperfpga.CasperFpga('192.168.20.60')
time.sleep(3)
if (!fpga.is_connected()):
    print("Did not connect to fpga")
    die = 5 / 0

while(1):
    q = read_q_values(fpga)
    i = read_i_values(fpga)

    mag = np.hypot(np.array(i), np.array(q))

    line.set_xdata(np.arange(len(mag)))
    line.set_ydata(mag)
    ax.relim()
    ax.autoscale_view()

    fig.canvas.draw()
    fig.canvas.flush_events()

    time.sleep(.2)
