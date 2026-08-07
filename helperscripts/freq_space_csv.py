import csv
import datetime
import time
import casperfpga
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

fpga = casperfpga.CasperFpga("192.168.20.60")
time.sleep(3)
if not fpga.is_connected():
        print("Did not connect to fpga")
            die = 5 / 0

            while 1:
                    noise_space = []
                        peak_space = []

                            for i in range(21):
                                        time.sleep(0.1)

                                                fpga.write_int("Subsystem7_freq_shift_index", i)

                                                        peak_val = fpga.read_int("out_peak_val")
                                                                mean_val = fpga.read_int("out_noise_mean")

                                                                        noise_space.append(mean_val)
                                                                                peak_space.append(peak_val)

                                                                                    print("Peak space:", peak_space)
                                                                                        print("Noise space:", noise_space)

                                                                                            # Generate ISO timestamp for filename (e.g., fpga_data_20260804_170645.csv)
                                                                                                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                                                                                    filename = f"fpga_data_{timestamp}.csv"

                                                                                                        # Write iteration results to CSV
                                                                                                            with open(filename, mode="w", newline="") as file:
                                                                                                                        writer = csv.writer(file)
                                                                                                                                writer.writerow(["freq_shift_index", "peak_val", "noise_mean"])
                                                                                                                                        for idx, (p_val, n_val) in enumerate(zip(peak_space, noise_space)):
                                                                                                                                                        writer.writerow([idx, p_val, n_val])

                                                                                                                                                            print(f"Saved: {filename}")
