from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_swagger_ui_plain() -> None:
    # Copy of https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_application.py#L24-L32
    response = client.get("/swaggerui-plain")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "swagger-ui-dist" in response.text
    assert (
        "oauth2RedirectUrl: window.location.origin + '/docs/oauth2-redirect'"
        in response.text
    )


def test_swagger_ui_custom() -> None:
    # Copy of https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_tutorial/test_custom_docs_ui/test_tutorial001.py#L20-L26
    response = client.get("/swaggerui-custom")
    assert response.status_code == 200, response.text
    assert (
        "https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js" in response.text
    )
    assert "https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" in response.text
    # Copy of https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_swagger_ui_init_oauth.py#L17-L23
    assert "ui.initOAuth" in response.text
    assert '"appName": "Test Application"' in response.text
    assert '"clientId": "the-application-clients"' in response.text
    # Copy of https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_no_swagger_ui_redirect.py#L15-L21C1
    assert "oauth2RedirectUrl" not in response.text

    # Copy of https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_tutorial/test_configure_swagger_ui/test_tutorial001.py#L8-L35 and https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_tutorial/test_configure_swagger_ui/test_tutorial002.py#L8-L38 and https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_tutorial/test_configure_swagger_ui/test_tutorial003.py#L8-L38
    assert (
        '"deepLinking": false,' in response.text
    ), "overridden configs should be preserved"
    assert (
        '"deepLinking": true' not in response.text
    ), "overridden configs should not include the old value"
    assert (
        '"syntaxHighlight": false' in response.text
    ), "syntaxHighlight should be included and converted to JSON"
    assert (
        '"syntaxHighlight.theme": "obsidian"' in response.text
    ), "parameters with middle dots should be included in a JSON compatible way"
    assert (
        '"dom_id": "#swagger-ui"' in response.text
    ), "default configs should be preserved"
    assert "presets: [" in response.text, "default configs should be preserved"
    assert (
        "SwaggerUIBundle.presets.apis," in response.text
    ), "default configs should be preserved"
    assert (
        "SwaggerUIBundle.SwaggerUIStandalonePreset" in response.text
    ), "default configs should be preserved"
    assert (
        '"layout": "BaseLayout",' in response.text
    ), "default configs should be preserved"
    assert (
        '"showExtensions": true,' in response.text
    ), "default configs should be preserved"
    assert (
        '"showCommonExtensions": true,' in response.text
    ), "default configs should be preserved"
