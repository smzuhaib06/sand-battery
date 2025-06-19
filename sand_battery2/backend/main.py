from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}

@app.get("/data")
def get_sensor_data():
    return {
        "voltage": 3.7,
        "current": 100,
        "power": 370,
        "status": "Discharging"
    }

@app.get("/ai_status")
def get_ai_data():
    return {
        "backup_time": "2 hours",
        "recommendation": "Discharge",
        "mode": "Auto"
    }

@app.post("/control")
def control_device(gpio: str = Form(...), value: str = Form(...)):
    print(f"GPIO: {gpio}, Value: {value}")
    return {"status": "success", "gpio": gpio, "value": value}
