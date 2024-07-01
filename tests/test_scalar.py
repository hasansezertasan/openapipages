import pytest
from httpx import AsyncClient

from .main import app


@pytest.mark.asyncio()
async def test_scalar_plain() -> None:
    async with AsyncClient(app=app, base_url="http://testserver/") as client:
        response = await client.get("/scalar-plain")
        assert response.status_code == 200, response.text
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "@scalar/api-reference" in response.text


@pytest.mark.asyncio()
async def test_scalar_custom() -> None:
    async with AsyncClient(app=app, base_url="http://testserver/") as client:
        response = await client.get("/scalar-custom")
        assert response.status_code == 200, response.text
        assert "https://cdn.jsdelivr.net/npm/@scalar/api-reference" in response.text
