import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from tests.main import app


@pytest.mark.asyncio
async def test_scalar_plain() -> None:
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://testserver/"
    ) as client:
        response = await client.get("/scalar-plain")
        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "@scalar/api-reference" in response.text


@pytest.mark.asyncio
async def test_scalar_custom() -> None:
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://testserver/"
    ) as client:
        response = await client.get("/scalar-custom")
        assert response.status_code == status.HTTP_200_OK, response.text
        assert "https://cdn.jsdelivr.net/npm/@scalar/api-reference" in response.text
