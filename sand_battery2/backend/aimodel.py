# ai_model.py
import joblib
import pandas as pd

# Load the AI model from disk (only once)
model = joblib.load("control_model.pkl")

def predict_action(voltage, current, power, hour):
    input_data = pd.DataFrame([{
        "voltage": voltage,
        "current": current,
        "power": power,
        "hour": hour
    }])
    prediction = model.predict(input_data)[0]
    return prediction
