# app/auth.py
from fastapi import APIRouter, HTTPException, Depends, Response, Request
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import jwt
from typing import Optional
import os

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-please")
JWT_ALG = "HS256"
ACCESS_EXPIRE_MINUTES = 30

# Simple token revocation store (replace with Redis in prod)
_revoked = set()

class LoginIn(BaseModel):
    email: EmailStr
    password: str

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None):
    now = datetime.utcnow()
    exp = now + (expires_delta or timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    payload = {"sub": subject, "iat": now.timestamp(), "exp": exp.timestamp()}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

@router.post("/login")
def login(payload: LoginIn, response: Response):
    # TODO: replace with secure user lookup & password verify (bcrypt)
    if payload.email != "demo@example.com" or payload.password != "demo":
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_access_token(payload.email)
    response.set_cookie("access_token", token, httponly=True, secure=True, samesite="lax")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(request: Request):
    token = request.cookies.get("access_token")
    if token:
        _revoked.add(token)
    return {"msg": "logged out"}

def verify_token(token: str):
    if token in _revoked:
        raise HTTPException(401, "token_revoked")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="token_expired")
    except Exception:
        raise HTTPException(status_code=401, detail="token_invalid")
