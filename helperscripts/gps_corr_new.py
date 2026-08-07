import casperfpga
import paho.mqtt.client as mqtt
import json
import time
import datetime
import csv
import sys  # Added for proper exiting

lat = None
long = None

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Successfully connected to broker.")
        client.subscribe("afe/data/gps")
    else:
        print(f"Failed to connect. Reason code: {reason_code}")

def on_message(client, userdata, msg):
    global lat, long  # Fix: explicitly reference the global variables
    try:
        payload = msg.payload.decode('utf-8')
        message = json.loads(payload)
        lat = message["lat"]
        long = message["lon"]
    except Exception as e:
        print(f"Error decoding MQTT message: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

broker = "localhost"
port = 1883

print(f"Connecting to {broker}...")
client.connect(broker, port, keepalive=60)

# Fix: Start a background thread to process network traffic
client.loop_start()

fpga = casperfpga.CasperFpga("192.168.20.60")
time.sleep(3)
if not fpga.is_connected():
    print("Did not connect to fpga")
    sys.exit(1)  # Fix: exit cleanly instead of throwing ZeroDivisionError

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"unh_collection/fpga_data_{timestamp}.csv"

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["time", "lat", "lon", "freq_index", "peak_val", "noise_mean"])

while True:
    noise_space = []
    peak_space = []

    # Fix: Open the file once per 21-iteration sweep instead of 21 times
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        for i in range(21):
            fpga.write_int("Subsystem7_freq_shift_index", i)
            time.sleep(0.5)

            peak_val = fpga.read_int("out_peak_val")
            mean_val = fpga.read_int("out_noise_mean")

            noise_space.append(mean_val)
            peak_space.append(peak_val)

            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            writer.writerow([current_time, lat, long, i, peak_val, mean_val])
        
    print("___________________________________________________________________")
    print(peak_space)
    print(noise_space)
    print("___________________________________________________________________")
    print(f"Saved: {filename}")
