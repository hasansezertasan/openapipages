"""Unit tests for ``Base`` — the shared string-building helpers and defaults.

These exercise the tag-generation logic in isolation (no HTTP framework), which
the integration tests only reach indirectly through a rendered page.
"""

from openapipages.base import Base


def _base() -> Base:
    return Base(title="Title", js_url="https://cdn.example/app.js")


def test_defaults() -> None:
    base = _base()
    assert base.openapi_url == "/openapi.json"
    assert base.favicon_url == "/favicon.ico"
    assert base.head_js_urls == []
    assert base.tail_js_urls == []
    assert base.head_css_urls == []


def test_head_css_str_from_explicit_urls() -> None:
    result = _base().get_head_css_str(["a.css", "b.css"])
    assert result == (
        '<link type="text/css" rel="stylesheet" href="a.css">\n'
        '<link type="text/css" rel="stylesheet" href="b.css">'
    )


def test_head_js_str_from_explicit_urls() -> None:
    assert _base().get_head_js_str(["a.js"]) == '<script src="a.js"></script>'


def test_tail_js_str_from_explicit_urls() -> None:
    assert _base().get_tail_js_str(["a.js"]) == '<script src="a.js"></script>'


def test_helpers_fall_back_to_instance_fields_when_urls_none() -> None:
    # With the default (empty) field lists, each helper yields an empty string.
    base = _base()
    assert not base.get_head_css_str()
    assert not base.get_head_js_str()
    assert not base.get_tail_js_str()


def test_helpers_use_instance_fields() -> None:
    base = Base(
        title="Title",
        js_url="app.js",
        head_js_urls=["head.js"],
        tail_js_urls=["tail.js"],
        head_css_urls=["head.css"],
    )
    assert base.get_head_js_str() == '<script src="head.js"></script>'
    assert base.get_tail_js_str() == '<script src="tail.js"></script>'
    assert base.get_head_css_str() == (
        '<link type="text/css" rel="stylesheet" href="head.css">'
    )
