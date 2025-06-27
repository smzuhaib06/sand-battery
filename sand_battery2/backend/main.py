 main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import board
import busio
from adafruit_ina219 import INA219

# Set up I2C and sensor
i2c_bus = busio.I2C(board.SCL, board.SDA)
ina = INA219(i2c_bus)
# optional; default config works for most 0.1 ohm shunt setups

# FastAPI app
app = FastAPI()

# CORS for cross-device access (e.g., from Jetson/PC)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend device's IP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "INA219 Sensor API Running"}

@app.get("/data")
def get_sensor_data():
    try:
        voltage = round(ina.bus_voltage + (ina.shunt_voltage / 1000), 2)  # Total voltage
        current = round(ina.current, 2)  # mA
        power = round(ina.power, 2)  # mW
        status = "Discharging" if current > 0 else "Idle"
        return {
            "voltage": voltage,
            "current": current,
            "power": power,
            "status": status
        }
    except Exception as e:
        return {"error": str(e)}
