import time
from datetime import datetime, timezone

SENSORS = {
    "28-011912555951": "ambient_room",
    "28-011912765725": "probe_target"
}

BASE_PATH = "/sys/bus/w1/devices"

def read_temp(sensor_id):
    with open(f"{BASE_PATH}/{sensor_id}/temperature", "r") as f:
        return int(f.read().strip()) / 1000.0

while True:
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    readings = []

    for sensor_id, name in SENSORS.items():
        temp_c = read_temp(sensor_id)
        readings.append((name, temp_c))
        print(f"{timestamp} | {name}: {temp_c:.2f} °C")

    print("-" * 40)
    time.sleep(5)
