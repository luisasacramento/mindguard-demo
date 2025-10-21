# tests/test_auth.py
from fastapi.testclient import TestClient
from app.auth import router as auth_router
from fastapi import FastAPI

# Cria um app FastAPI de teste
app = FastAPI()
app.include_router(auth_router, prefix="/auth")

client = TestClient(app)

def test_login_success():
    response = client.post("/auth/login", json={
        "email": "demo@example.com",
        "password": "demo"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.cookies.get("access_token") is not None

def test_login_fail():
    response = client.post("/auth/login", json={
        "email": "demo@example.com",
        "password": "wrong-password"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"

def test_logout():
    # Primeiro, loga para gerar cookie
    login_resp = client.post("/auth/login", json={
        "email": "demo@example.com",
        "password": "demo"
    })
    token = login_resp.cookies.get("access_token")
    # Chama logout com cookie
    logout_resp = client.post("/auth/logout", cookies={"access_token": token})
    assert logout_resp.status_code == 200
    assert logout_resp.json()["msg"] == "logged out"

def test_verify_token_revoked():
    # Gera token manualmente
    from app.auth import create_access_token, _revoked, verify_token
    token = create_access_token("demo@example.com")
    _revoked.add(token)
    import pytest
    with pytest.raises(Exception):
        verify_token(token)
