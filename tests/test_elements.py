import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from tests.main import app


@pytest.mark.asyncio
async def test_elements() -> None:
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://testserver/",
    ) as client:
        response = await client.get("/elements")
        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        js_tag = (
            '<script src="https://unpkg.com/@stoplight/elements/web-components.min.js">'
        )
        css_tag = '<link type="text/css" rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">'
        assert response.text.count(js_tag) == 1, (
            "js_url should be injected exactly once"
        )
        assert response.text.count(css_tag) == 1, (
            "css_url should be injected exactly once"
        )
