"""Unit tests for each renderer's ``render()`` option branches.

Renderers are instantiated and rendered directly (no ASGI/httpx), so these tests
isolate the option logic — ``init_oauth`` on/off, ``oauth2_redirect_url=None``,
parameter merging, ``proxy_url``, google-fonts toggling — that the integration
tests only cover through a full HTTP round-trip.
"""

import pytest
from openapipages import Elements, RapiDoc, ReDoc, Scalar, SwaggerUI


class TestSwaggerUI:
    def test_defaults_inject_urls_and_spec(self) -> None:
        html = SwaggerUI(title="X").render()
        assert "swagger-ui-bundle.js" in html
        assert "swagger-ui.css" in html
        assert '"url": "/openapi.json"' in html

    def test_default_oauth2_redirect_present(self) -> None:
        assert "oauth2RedirectUrl:" in SwaggerUI(title="X").render()

    def test_oauth2_redirect_none_is_omitted(self) -> None:
        html = SwaggerUI(title="X", oauth2_redirect_url=None).render()
        assert "oauth2RedirectUrl:" not in html

    def test_init_oauth_absent_by_default(self) -> None:
        assert "ui.initOAuth(" not in SwaggerUI(title="X").render()

    def test_init_oauth_present_when_configured(self) -> None:
        html = SwaggerUI(title="X", init_oauth={"clientId": "abc"}).render()
        assert "ui.initOAuth(" in html
        assert '"clientId": "abc"' in html

    def test_parameters_override_defaults(self) -> None:
        # default_parameters sets deepLinking True; an override must win.
        html = SwaggerUI(
            title="X",
            swagger_ui_parameters={"deepLinking": False},
        ).render()
        assert '"deepLinking": false' in html

    def test_extra_presets_are_appended(self) -> None:
        html = SwaggerUI(title="X", swagger_ui_presets=["My.Preset"]).render()
        assert "My.Preset" in html

    def test_noscript_fallback_present(self) -> None:
        # The <noscript> fallback is this PR's behavior change; pin it in the
        # always-run suite rather than relying only on the (CDN-dependent) e2e.
        html = SwaggerUI(title="X").render()
        assert "<noscript>" in html
        assert "requires Javascript to function" in html


class TestReDoc:
    def test_defaults_inject_js_and_spec(self) -> None:
        html = ReDoc(title="X").render()
        assert "redoc.standalone.js" in html
        assert '"/openapi.json"' in html

    def test_google_fonts_present_by_default(self) -> None:
        assert "fonts.googleapis.com" in ReDoc(title="X").render()

    def test_google_fonts_can_be_disabled(self) -> None:
        assert (
            "fonts.googleapis.com"
            not in ReDoc(title="X", with_google_fonts=False).render()
        )

    def test_ui_parameters_merge(self) -> None:
        # hideDownloadButton is not in default_parameters, and asserting the
        # rendered key/value proves the user dict actually merged in (rather
        # than a "true" that a default like "wrap": true would satisfy anyway).
        html = ReDoc(title="X", ui_parameters={"hideDownloadButton": True}).render()
        assert '"hideDownloadButton": true' in html


class TestScalar:
    def test_defaults_inject_url_without_proxy(self) -> None:
        html = Scalar(title="X").render()
        assert 'data-url="/openapi.json"' in html
        assert "data-proxy-url" not in html

    def test_proxy_url_adds_attribute(self) -> None:
        html = Scalar(title="X", proxy_url="https://proxy.example").render()
        assert 'data-proxy-url="https://proxy.example"' in html


class TestRapiDoc:
    def test_spec_url_and_js_injected(self) -> None:
        html = RapiDoc(title="X").render()
        assert '<rapi-doc spec-url="/openapi.json">' in html
        assert "rapidoc-min.js" in html


class TestElements:
    def test_api_description_url_and_assets_injected(self) -> None:
        html = Elements(title="X").render()
        assert 'apiDescriptionUrl="/openapi.json"' in html
        assert "web-components.min.js" in html
        assert "styles.min.css" in html


@pytest.mark.parametrize("renderer_cls", [SwaggerUI, ReDoc, RapiDoc, Elements, Scalar])
def test_user_supplied_url_lists_are_rendered(
    renderer_cls: type[SwaggerUI | ReDoc | RapiDoc | Elements | Scalar],
) -> None:
    """User-provided head/tail JS and head CSS URLs reach the rendered HTML.

    These ``Base`` list fields are a documented public feature but were only
    exercised with empty lists, so a regression dropping the user list would
    have gone unnoticed. Each renderer's template emits all three slots.
    """
    html = renderer_cls(
        title="X",
        head_js_urls=["https://cdn.example/head.js"],
        tail_js_urls=["https://cdn.example/tail.js"],
        head_css_urls=["https://cdn.example/head.css"],
    ).render()
    assert '<script src="https://cdn.example/head.js"></script>' in html
    assert '<script src="https://cdn.example/tail.js"></script>' in html
    assert (
        '<link type="text/css" rel="stylesheet" href="https://cdn.example/head.css">'
        in html
    )
