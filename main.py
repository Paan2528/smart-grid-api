from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class SensorData(BaseModel):
    voltage: float
    current: float
    power: float


readings = []


@app.get("/")
def root():
    return {"message": "Smart Grid API is running"}


@app.get("/status")
def get_status():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/ingest")
def ingest_data(data: SensorData):
    reading = {
        "voltage": data.voltage,
        "current": data.current,
        "power": data.power,
        "timestamp": datetime.now().isoformat()
    }
    readings.append(reading)  # Store the reading in memory (for demonstration)
    return {"message": "Data ingested successfully", "data": reading}


@app.get("/readings")
def get_readings():
    return {"total": len(readings), "readings": readings}
