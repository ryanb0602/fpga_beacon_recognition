import casperfpga
import time # Added missing import for time.sleep()

def uint16_to_int16(val):
    # If the value is greater than 32767, subtract 65536 (2^16)
    return val - 65536 if val >= 0x8000 else val

fpga = casperfpga.CasperFpga('192.168.20.60')
time.sleep(3)

if not fpga.is_connected():
    print("Did not connect to fpga")
    # Intentional crash if not connected
    die = 5 / 0 

samples = 500
search_R = range(-56, 12)

for x in search_R:
    # It is usually best practice to reset your accumulators for each new 'x' value
    # unless you intentionally want a running average across all search_R iterations.
    accum = 0
    samarr = []
    
    for i in range(samples):
        fpga.write_int('Subsystem7_cic_bit_shift', x)
        
        # Read the raw integer from the FPGA
        raw_sam = fpga.read_int('Subsystem7_cic_out')
        
        # Note: You defined uint16_to_int16 earlier but didn't use it. 
        # If your FPGA is outputting signed 16-bit data, apply it here:
        sam = uint16_to_int16(raw_sam) 
        
        accum += sam
        samarr.append(sam)
    
    # 1. Calculate the Mean
    mean = accum / len(samarr)
    
    # 2. Calculate the Average Difference from the Mean (Mean Absolute Deviation)
    avg_dev = sum(abs(val - mean) for val in samarr) / len(samarr)
    
    print(f"Shift: {x} | Mean: {mean:.2f} | Avg Deviation: {avg_dev:.2f}")
