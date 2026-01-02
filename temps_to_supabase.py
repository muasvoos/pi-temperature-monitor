import os
import time
from datetime import datetime, timezone

import requests

# Load env file (simple loader)
ENV_PATH = os.path.expanduser("~/supabase.env")
if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_KEY = os.environ["SUPABASE_ANON_KEY"]
DEVICE_ID = os.environ.get("DEVICE_ID", "pi4")

SENSORS = {
    "28-011912555951": "ambient_room",
    "28-011912765725": "probe_target",
}

BASE_PATH = "/sys/bus/w1/devices"

def read_temp_c(sensor_id: str) -> float:
    with open(f"{BASE_PATH}/{sensor_id}/temperature", "r") as f:
        return int(f.read().strip()) / 1000.0

def post_rows(rows):
    url = f"{SUPABASE_URL}/rest/v1/temperature_readings"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }
    r = requests.post(url, headers=headers, json=rows, timeout=10)
    if r.status_code >= 300:
        raise RuntimeError(f"Supabase error {r.status_code}: {r.text}")

def main():
    while True:
        ts_utc = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        rows = []
        for sensor_id, name in SENSORS.items():
            temp_c = read_temp_c(sensor_id)
            rows.append({
                "device_id": DEVICE_ID,
                "sensor_id": sensor_id,
                "sensor_name": name,
                "temp_c": round(temp_c, 3),
                "ts_utc": ts_utc,
            })
            print(f"{ts_utc} | {name}: {temp_c:.2f} °C")

        try:
            post_rows(rows)
            print("Uploaded ✅")
        except Exception as e:
            print(f"Upload failed: {e}")

        print("-" * 40)
        time.sleep(10)

if __name__ == "__main__":
    main()
