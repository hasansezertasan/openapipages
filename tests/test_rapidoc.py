import pytest
from httpx import AsyncClient

from .main import app


@pytest.mark.asyncio()
async def test_rapidoc() -> None:
    async with AsyncClient(app=app, base_url="http://testserver/") as client:
        response = await client.get("/rapidoc")
        assert response.status_code == 200, response.text
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "rapidoc/dist/rapidoc-min.js" in response.text
