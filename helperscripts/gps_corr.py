import casperfpga
import paho.mqtt.client as mqtt
import json
import time
import datetime
import csv

lat = None
long = None

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Successfully connected to broker.")
        client.subscribe("afe/data/gps")
    else:
        print(f"Failed to connect. Reason code: {reason_code}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    message = json.loads(payload)
    lat = message["lat"]
    long = message["lon"]
    

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

broker = "localhost"
port = 1883

print(f"Connecting to {broker}...")
client.connect(broker, port, keepalive=60)

fpga = casperfpga.CasperFpga("192.168.20.60")
time.sleep(3)
if not fpga.is_connected():
    print("Did not connect to fpga")
    die = 5 / 0


timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"fpga_data_{timestamp}.csv"


with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["time", "lat","lon", "freq_index", "peak_val", "noise_mean"])

while 1:
    noise_space = []
    peak_space = []

    for i in range(21):

        fpga.write_int("Subsystem7_freq_shift_index", i)

        time.sleep(.5)

        peak_val = fpga.read_int("out_peak_val")
        mean_val = fpga.read_int("out_noise_mean")

        noise_space.append(mean_val)
        peak_space.append(peak_val)

        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([current_time, lat, long, i, peak_val, mean_val])
        
    print("___________________________________________________________________")
    print(peak_space)
    print(noise_space)
    print("___________________________________________________________________")

    print(f"Saved: {filename}")

