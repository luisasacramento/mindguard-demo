from fastapi import FastAPI, HTTPException
from app.ml_model import load_model, predict_risk
from app.storage import Storage
import os

app = FastAPI(title="MindGuard Demo")
storage = Storage("storage.json")
model = None

@app.on_event("startup")
def startup_event():
    global model
    model = load_model()

@app.post("/consent")
def give_consent(user_id: str, consent: bool):
    storage.set_consent(user_id, consent)
    return {"message": f"Consent updated to {consent}"}

@app.post("/submit_bet")
def submit_bet(user_id: str, amount: float, frequency: int):
    if not storage.has_consent(user_id):
        raise HTTPException(status_code=403, detail="Consent not given")
    storage.add_bet(user_id, amount, frequency)
    return {"message": "Bet recorded"}

@app.get("/risk/{user_id}")
def get_risk(user_id: str):
    if not storage.has_consent(user_id):
        raise HTTPException(status_code=403, detail="Consent not given")
    data = storage.get_user_data(user_id)
    if not data:
        raise HTTPException(status_code=404, detail="No data for user")
    risk = predict_risk(model, data)
    return {"risk": risk}

@app.post("/intervene/{user_id}")
def intervene(user_id: str):
    if not storage.has_consent(user_id):
        raise HTTPException(status_code=403, detail="Consent not given")
    return {"message": f"Intervention triggered for {user_id}"}

@app.get("/report/{user_id}")
def report(user_id: str):
    return storage.get_user_data(user_id)

# 🚨 Endpoint inseguro de demonstração (vai ser detectado por Semgrep)
@app.get("/admin/run_eval")
def insecure_admin(cmd: str):
    # não faça isso em produção!
    os.system(cmd)
    return {"executed": cmd}
