import casperfpga

def to_signed(val, bits):
    if val & (1 << (bits - 1)):
        val -= (1 << bits)
    return val

def fbp17(raw18):
    return to_signed(raw18, 18) / (1 << 17)

def unpack(bit_arr):
    ELEM_BYTES = 16
    MASK18 = 0x3FFFF

    results = []
    for i in range(0, 64 * ELEM_BYTES, ELEM_BYTES):
        chunk = bit_arr[i:i + ELEM_BYTES]
        val128 = int.from_bytes(chunk, "big")
        top72 = val128 >> 56

        e0 = (top72 >> 54) & MASK18
        e1 = (top72 >> 36) & MASK18
        e2 = (top72 >> 18) & MASK18
        e3 =  top72        & MASK18

        results.append([fbp17(e) for e in (e0, e1, e2, e3)])

def read_i_values(fpga):
    segment_one = fpga.read("shared_bram", 8192, 0)
    segment_two = fpga.read("shared_bram1", 8192, 0)
    segment_three = fpga.read("shared_bram2", 8192, 0)
    segment_four = fpga.read("shared_bram3", 8192, 0)

    seg_a_unpacked = unpack(segment_one)
    seg_b_unpacked = unpack(segment_two)
    seg_c_unpacked = unpack(segment_three)
    seg_d_unpacked = unpack(segment_four)

    result = [x for group in zip(seg_a_unpacked, seg_b_unpacked, seg_c_unpacked, seg_d_unpacked) for x in group]
    
    return result

def read_q_values(fpga):
    segment_one = fpga.read("shared_bram", 8192, 0)
    segment_two = fpga.read("shared_bram1", 8192, 0)
    segment_three = fpga.read("shared_bram2", 8192, 0)
    segment_four = fpga.read("shared_bram3", 8192, 0)

    seg_a_unpacked = unpack(segment_one)
    seg_b_unpacked = unpack(segment_two)
    seg_c_unpacked = unpack(segment_three)
    seg_d_unpacked = unpack(segment_four)

    result = [x for group in zip(seg_a_unpacked, seg_b_unpacked, seg_c_unpacked, seg_d_unpacked) for x in group]
    
    return result
