import csv
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

filename = input("Input target file: ")

data_array = []
outcomes = []

with open(filename, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    next(reader) 
    
    data_array = list(reader)


for row in data_array:
    snr = int(row[0])
    wifi_db = int(row[1])
    exp_phase_shift = int(row[2])
    exp_dopp = int(row[3])
    found_phase = float(row[4])
    found_dopp = int(row[5])

    if (np.abs(exp_phase_shift - found_phase) < 50 and np.abs(exp_dopp - found_dopp) < 50):
        outcomes.append(((snr, wifi_db), 1))
    else:
        outcomes.append(((snr, wifi_db), 0))

tracker = defaultdict(lambda: [0, 0])

for key, outcome in outcomes:
    tracker[key][0] += outcome 
    tracker[key][1] += 1

accuracies = {}
for key, (successes, attempts) in tracker.items():
    accuracies[key] = successes / attempts

for (snr, wifi_db), accuracy in accuracies.items():
    print(f"SNR: {snr}, WiFi dB: {wifi_db} | Accuracy: {accuracy:.2%}")

snr_vals = [key[0] for key in accuracies.keys()]
wifi_vals = [key[1] for key in accuracies.keys()]
acc_vals = list(accuracies.values())

plt.figure(figsize=(10, 8))

scatter = plt.scatter(snr_vals, wifi_vals, c=acc_vals, cmap='RdYlGn', s=500, marker='s')

cbar = plt.colorbar(scatter)
cbar.set_label('Accuracy (0.0 to 1.0)')

plt.title('Accuracy Colormap: SNR vs WiFi dB')
plt.xlabel('SNR')
plt.ylabel('WiFi dB')
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()
