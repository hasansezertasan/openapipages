from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_redoc_plain() -> None:
    # Copy of  https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_application.py#L42-L46
    response = client.get("/redoc-plain")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "redoc@next" in response.text


def test_redoc_custom() -> None:
    # Copy of  https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_tutorial/test_custom_docs_ui/test_tutorial001.py#L35-L38
    response = client.get("/redoc-custom")
    assert response.status_code == 200, response.text
    assert "https://unpkg.com/redoc@next/bundles/redoc.standalone.js" in response.text
