from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_elements() -> None:
    response = client.get("/elements")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "@stoplight/elements/web-components.min.js" in response.text
    assert "@stoplight/elements/styles.min.css" in response.text
