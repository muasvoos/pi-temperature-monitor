import glob
import time

base_dir = "/sys/bus/w1/devices/"
device_folders = glob.glob(base_dir + "28-*")

def read_temp(sensor):
    with open(sensor + "/temperature", "r") as f:
        temp_milli = int(f.read().strip())
        return temp_milli / 1000.0

while True:
    for sensor in device_folders:
        temp = read_temp(sensor)
        print(f"{sensor.split('/')[-1]}: {temp:.2f} °C")
    print("----")
    time.sleep(5)

