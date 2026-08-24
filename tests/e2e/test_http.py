"""HTTP e2e: the real (subprocess) server serves every renderer page.

Complements the browser tests by exercising the actual ASGI stack over the wire
— not the in-process ``TestClient`` — before any JavaScript is involved.
"""

from __future__ import annotations

import httpx
import pytest

from tests.e2e.app import API_TITLE, OPENAPI_URL, RENDERER_PATHS


@pytest.mark.parametrize("renderer", list(RENDERER_PATHS))
def test_page_served_over_the_wire(base_url: str, renderer: str) -> None:
    """Each renderer route returns 200 HTML that points at the spec URL."""
    response = httpx.get(f"{base_url}{RENDERER_PATHS[renderer]}", timeout=10.0)
    assert response.status_code == httpx.codes.OK, response.text
    assert response.headers["content-type"].startswith("text/html")
    assert OPENAPI_URL in response.text, (
        f"{renderer}: served page does not reference {OPENAPI_URL!r}"
    )


def test_spec_carries_expected_title(base_url: str) -> None:
    """The served spec has the title the browser tests assert on."""
    response = httpx.get(f"{base_url}{OPENAPI_URL}", timeout=10.0)
    assert response.status_code == httpx.codes.OK, response.text
    assert response.json()["info"]["title"] == API_TITLE
