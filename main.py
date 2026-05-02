from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI()

# Database Setup


def init_db():
    # chreate a file to store data (connect SQLite)
    conn = sqlite3.connect("grid.db")
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS readings (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 voltage REAL,
                 current REAL,
                 power REAL,
                 timestamp TEXT
                 )
                 """)

    conn.commit()
    conn.close()

# --------------------------------------------
# call the init_db when the server starts
# ----------Pydantic model for sensor data----------------


class SensorData(BaseModel):
    voltage: float
    current: float
    power: float
# ------------------------------------------------------------
# Endpoints
# --------------------------------------------


@app.get("/status")
def get_status():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/ingest")
def ingest_data(data: SensorData):
    timestamp = datetime.now().isoformat()
    # store the data in the database
    conn = sqlite3.connect("grid.db")
    conn.execute(
        "INSERT INTO readings (voltage, current, power,timestamp) VALUES (?, ?, ?, ?)",
        (data.voltage, data.current, data.power, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return {
        "message": "Data saved successfully",
        "data": {
            "votage": data.voltage,
            "current": data.current,
            "power": data.power,
            "timestamp": timestamp
        }
    }


@app.get("/readings")
def get_readings(limit: int = 10):
    conn = sqlite3.connect("grid.db")
    # fetch the latest readings from the database
    rows = conn.execute(
        "SELECT voltage, current, power, timestamp FROM readings ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()

    # change rows to a list of dicts
    result = [
        {
            "id": row[0],
            "voltage": row[1],
            "current": row[2],
            "power": row[3],
            "timestamp": row[4]
        }
        for row in rows
    ]

    return {"total": len(result), "readings": result}
