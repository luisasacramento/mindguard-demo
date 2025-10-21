from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_login_logout():
    r = client.post("/login", json={"email":"demo@example.com","password":"demo"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    cookies = r.cookies
    assert "access_token" in cookies

    # Logout revoga token
    r2 = client.post("/logout", cookies=cookies)
    assert r2.status_code == 200
