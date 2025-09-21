from fastapi import FastAPI, HTTPException
from app.storage import Storage
import os

app = FastAPI(title="MindGuard Demo Simplificada")
storage = Storage("storage.json")

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
    # Risco simulado: só retorna se a aposta é alta
    risk = "high" if data["amount"] > 100 else "low"
    return {"risk": risk}

@app.post("/intervene/{user_id}")
def intervene(user_id: str):
    if not storage.has_consent(user_id):
        raise HTTPException(status_code=403, detail="Consent not given")
    return {"message": f"Intervention triggered for {user_id}"}

@app.get("/report/{user_id}")
def report(user_id: str):
    return storage.get_user_data(user_id)

# 🚨 Vulnerabilidade proposital para testes SAST/DAST
@app.get("/admin/run_eval")
def insecure_admin(cmd: str):
    # Comando arbitrário (danger zone)
    os.system(cmd)
    return {"executed": cmd}

# 🚨 Vulnerabilidade proposital: exposição de variável de ambiente
@app.get("/leak_env")
def leak_env(secret_key: str = "SECRET_KEY"):
    return {"secret": os.environ.get(secret_key, "not_set")}
