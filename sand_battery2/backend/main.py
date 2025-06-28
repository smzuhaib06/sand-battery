# main.py
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import board
import busio
from adafruit_ina219 import INA219
from control_logic import control_gpio

app = FastAPI()

# CORS setup for Jetson or any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with Jetson's IP for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INA219 setup
i2c_bus = busio.I2C(board.SCL, board.SDA)
ina = INA219(i2c_bus)

@app.get("/")
def root():
    return {"message": "Sand Battery API running on Raspberry Pi"}

@app.get("/data")
def get_sensor_data():
    try:
        voltage = round(ina.bus_voltage + (ina.shunt_voltage / 1000), 2)
        current = round(ina.current, 2)
        power = round(ina.power, 2)
        status = "Discharging" if current > 0 else "Idle"
        return {
            "voltage": voltage,
            "current": current,
            "power": power,
            "status": status
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/control")
def gpio_control(gpio: str = Form(...), value: str = Form(...)):
    state = value == "1"
    control_gpio(gpio, state)
    return {"message": f"Set {gpio} to {'ON' if state else 'OFF'}"}
