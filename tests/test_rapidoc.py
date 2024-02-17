from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_rapidoc() -> None:
    response = client.get("/rapidoc")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "rapidoc/dist/rapidoc-min.js" in response.text
