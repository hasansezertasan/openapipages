import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from tests.main import app


@pytest.mark.asyncio
async def test_elements() -> None:
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://testserver/"
    ) as client:
        response = await client.get("/elements")
        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "@stoplight/elements/web-components.min.js" in response.text
        assert "@stoplight/elements/styles.min.css" in response.text
