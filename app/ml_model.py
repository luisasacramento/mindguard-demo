import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

MODEL_PATH = "model.joblib"

def create_model():
    # gera dataset sintético
    data = pd.DataFrame({
        "amount": [10, 200, 50, 500, 20, 1000, 5, 70],
        "frequency": [1, 10, 2, 20, 1, 30, 1, 5],
        "risk": [0, 1, 0, 1, 0, 1, 0, 0],
    })
    X = data[["amount", "frequency"]]
    y = data["risk"]
    model = RandomForestClassifier()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print(f"Modelo salvo em {MODEL_PATH}")

def load_model():
    if not os.path.exists(MODEL_PATH):
        create_model()
    return joblib.load(MODEL_PATH)

def predict_risk(model, user_data):
    X = pd.DataFrame([user_data])
    return int(model.predict(X)[0])
