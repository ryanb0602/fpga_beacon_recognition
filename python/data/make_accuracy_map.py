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

    if (np.abs(exp_phase_shift - found_phase) < 10 and np.abs(exp_dopp - found_dopp) < 25):
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

est_snr = 11.37
est_wifi = -21.37
plt.scatter(est_snr, est_wifi, color='cyan', edgecolors='black', s=400, marker='*', label='Real-World Estimate')
plt.legend(loc='upper left')

plt.title('Accuracy Colormap: SNR vs WiFi dB')
plt.xlabel('SNR (dB)')
plt.ylabel('WiFi (dB)')
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()

snr_tracker = defaultdict(lambda: [0, 0])
wifi_tracker = defaultdict(lambda: [0, 0])

for (snr, wifi), (successes, attempts) in tracker.items():
    snr_tracker[snr][0] += successes
    snr_tracker[snr][1] += attempts
    
    wifi_tracker[wifi][0] += successes
    wifi_tracker[wifi][1] += attempts

# Calculate averages
snr_avg_acc = {snr: s/a for snr, (s, a) in snr_tracker.items()}
wifi_avg_acc = {wifi: s/a for wifi, (s, a) in wifi_tracker.items()}

# --- Plot Average Accuracy vs SNR ---
plt.figure(figsize=(10, 5))
sorted_snr = sorted(snr_avg_acc.items())
plt.plot([x[0] for x in sorted_snr], [y[1] for y in sorted_snr], marker='o', color='blue')
plt.title('Average Accuracy vs SNR (Averaged across all WiFi dB)')
plt.xlabel('SNR (dB)')
plt.ylabel('Average Accuracy')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# --- Plot Average Accuracy vs WiFi dB ---
plt.figure(figsize=(10, 5))
sorted_wifi = sorted(wifi_avg_acc.items())
plt.plot([x[0] for x in sorted_wifi], [y[1] for y in sorted_wifi], marker='s', color='red')
plt.title('Average Accuracy vs WiFi dB (Averaged across all SNR)')
plt.xlabel('WiFi (dB)')
plt.ylabel('Average Accuracy')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
