"""Browser render tests: every UI boots and renders the served spec.

Each test navigates a real Chromium page to a renderer's route and asserts the
spec's ``info.title`` becomes visible in the DOM. Because that title is distinct
from the page's HTML ``<title>``, it can only appear once the UI's JavaScript has
loaded from its CDN, executed, fetched ``/openapi.json``, and rendered it.

Playwright's text/CSS engines pierce *open* shadow DOM, so the same assertion
works for light-DOM UIs (SwaggerUI, ReDoc, Scalar) and web-component UIs that
render into open shadow roots (RapiDoc, Stoplight Elements).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from playwright.sync_api import expect

from tests.e2e.app import API_TITLE, RENDERER_PATHS

if TYPE_CHECKING:
    from playwright.sync_api import Page

# UI bundles are fetched from public CDNs, so allow a generous budget for the
# first paint (Elements and Scalar bundles are sizeable).
RENDER_TIMEOUT_MS = 45_000


@pytest.mark.parametrize("renderer", list(RENDERER_PATHS))
def test_ui_renders_spec_title(page: Page, base_url: str, renderer: str) -> None:
    """The API title from the spec renders in the browser for every UI.

    Raises:
        AssertionError: If the spec title never becomes visible in the DOM.
    """
    page.goto(f"{base_url}{RENDERER_PATHS[renderer]}", wait_until="load")
    title = page.get_by_text(API_TITLE).first
    try:
        expect(title).to_be_visible(timeout=RENDER_TIMEOUT_MS)
    except AssertionError as exc:
        snippet = page.inner_text("body")[:500]
        msg = (
            f"{renderer}: spec title {API_TITLE!r} never rendered within "
            f"{RENDER_TIMEOUT_MS}ms — the UI likely failed to boot or load the "
            f"spec. body snippet: {snippet!r}"
        )
        raise AssertionError(msg) from exc


@pytest.mark.parametrize("renderer", list(RENDERER_PATHS))
def test_page_tab_title_is_renderer_name(
    page: Page,
    base_url: str,
    renderer: str,
) -> None:
    """The HTML ``<title>`` (browser tab) is the renderer name we configured.

    This is a cheap check that the correct page was served, independent of the
    (slower) JS boot verified by :func:`test_ui_renders_spec_title`.
    """
    page.goto(f"{base_url}{RENDERER_PATHS[renderer]}", wait_until="domcontentloaded")
    expected = {
        "swaggerui": "SwaggerUI",
        "redoc": "ReDoc",
        "rapidoc": "RapiDoc",
        "elements": "Elements",
        "scalar": "Scalar",
    }[renderer]
    assert page.title() == expected, (
        f"{renderer}: expected tab title {expected!r}, got {page.title()!r}"
    )
