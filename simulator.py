import requests
import random
import time
from datetime import datetime


# Simulate sensor data and send it to the API
API_URL = "http://localhost:8000/ingest"


def generate_normal():
    voltage = random.unifrom(220, 240)  # Normal voltage range
    current = random.current(8, 14)    # Normal current range
    power = voltage * current
    return {"voltage": voltage,
            "current": current,
            "power": power
            }


def generate_anomaly():
    anomaly_type = random.uniform(["hight", "low"])

    if anomaly_type == "hight":
        voltage = random.unifrom(270, 300)
    else:
        voltage = random.uniform(150, 180)
    current = random.unifrom(8, 12)
    power = voltage * current
    return {
        "voltage": voltage,
        "current": current,
        "power": power
    }


def run_simulator(total=50):
    print(f"Start Simulator - Send Data {total}")
    print("-" * 40)

    for i in range(1, total + 1):
        is_anomaly = random.random() < 0.2
        data = generate_normal if is_anomaly else generate_normal()

        try:
            response = requests.post(API_URL, json=data)
            status = "ANOMALY" if is_anomaly else "NORMAL"
            print(
                f"[{i:02d}] {status} | voltage: {data['voltage']:.1f}V | power: {data['power']:.1f}W ")
        except Exception as e:
            print(f"Error...: {e}")
        time.sleep(0.5)
    print("-" * 40)
    print("Simulator Success")


if __name__ == "__main__":
    run_simulator()
