"""Progressive-enhancement e2e: the ``<noscript>`` fallback shows without JS.

Inspired by the no-JavaScript tests in ``xgovuk-flask-admin``. Every renderer
emits a ``<noscript>`` fallback telling the user to enable JavaScript.

A browser only renders ``<noscript>`` contents when scripting is disabled, so a
``java_script_enabled=False`` context is exactly what proves the fallback works.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.e2e.app import RENDERER_PATHS

if TYPE_CHECKING:
    from playwright.sync_api import Page

# Substring common to every fallback message
# (e.g. "ReDoc requires Javascript to function. Please enable it ...").
NOSCRIPT_TEXT = "requires Javascript to function"


@pytest.mark.parametrize("renderer", list(RENDERER_PATHS))
def test_noscript_fallback_visible_without_js(
    no_js_page: Page,
    base_url: str,
    renderer: str,
) -> None:
    """With JavaScript disabled, the renderer's ``<noscript>`` message shows.

    ``inner_text`` returns *rendered* text, and a browser only renders
    ``<noscript>`` contents when scripting is off — so this passing proves the
    fallback reaches the user. (Playwright's ``get_by_text`` engine skips
    ``<noscript>`` on purpose, hence the inner-text assertion.)
    """
    no_js_page.goto(
        f"{base_url}{RENDERER_PATHS[renderer]}",
        wait_until="domcontentloaded",
    )
    body_text = no_js_page.inner_text("body")
    assert NOSCRIPT_TEXT in body_text, (
        f"{renderer}: <noscript> fallback not rendered with JS disabled; "
        f"body text was {body_text!r}"
    )
