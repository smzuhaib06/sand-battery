# train_ai_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Separate features (X) and labels (y)
X = df[["voltage", "current", "power", "hour"]]
y = df["action"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "control_model.pkl")

print("✅ AI model trained and saved as control_model.pkl")
