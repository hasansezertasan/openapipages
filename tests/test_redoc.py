import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from tests.main import app


@pytest.mark.asyncio
async def test_redoc_plain() -> None:
    # Copy of  https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_application.py#L42-L46
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://testserver/"
    ) as client:
        response = await client.get("/redoc-plain")
        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "redoc@2" in response.text
        assert '"hideDownloadButton": false' in response.text


@pytest.mark.asyncio
async def test_redoc_custom() -> None:
    # Copy of  https://github.com/tiangolo/fastapi/blob/be876902554a0bd886167de144f0d593ed2e6ad7/tests/test_tutorial/test_custom_docs_ui/test_tutorial001.py#L35-L38
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://testserver/"
    ) as client:
        response = await client.get("/redoc-custom")
        assert response.status_code == status.HTTP_200_OK, response.text
        assert (
            "https://unpkg.com/redoc@next/bundles/redoc.standalone.js" in response.text
        )
