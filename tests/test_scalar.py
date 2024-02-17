from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_scalar_plain() -> None:
    response = client.get("/scalar-plain")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "@scalar/api-reference" in response.text


def test_scalar_custom() -> None:
    response = client.get("/scalar-custom")
    assert response.status_code == 200, response.text
    assert "https://cdn.jsdelivr.net/npm/@scalar/api-reference" in response.text
