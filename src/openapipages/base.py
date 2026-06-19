from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Annotated

from typing_extensions import Doc


@dataclass
class Base:
    """Base class for alternative API docs."""

    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """,
        ),
    ]
    js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the JavaScript.
            It is normally set to a CDN URL.
            """,
        ),
    ]
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that page should load and use.
            Default URL `/openapi.json`.
            """,
        ),
    ] = "/openapi.json"
    head_js_urls: Annotated[
        list[str],
        Doc(
            """
            A list of URLs to JavaScript files that should be loaded in the `<head>` tag.
            """,
        ),
    ] = field(default_factory=list)
    tail_js_urls: Annotated[
        list[str],
        Doc(
            """
            A list of URLs to JavaScript files that should be loaded at the end of the `<body>` tag.
            """,
        ),
    ] = field(default_factory=list)
    head_css_urls: Annotated[
        list[str],
        Doc(
            """
            A list of URLs to CSS files that should be loaded in the `<head>` tag.
            """,
        ),
    ] = field(default_factory=list)
    favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """,
        ),
    ] = "/favicon.ico"

    def render(self) -> str:
        """Generate and return the HTML response that loads the alternative API docs.

        Subclasses typically override this to inject UI-specific config; the default
        implementation renders `get_html_template()` with the common fields only.

        Returns:
            str: The generated HTML response as a string.
        """
        return self.get_html_template().format(
            title=self.title,
            favicon_url=self.favicon_url,
            head_css_str=self.get_head_css_str(),
            head_js_str=self.get_head_js_str(),
            tail_js_str=self.get_tail_js_str(),
        )

    def get_html_template(self) -> str:
        """Return the HTML template for the alternative API docs.

        Subclasses override this to provide a UI-specific template.
        """
        return ""

    def get_tail_js_str(self, urls: Sequence[str] | None = None) -> str:
        """Return the string of JavaScript URLs that should be loaded at the end of the `<body>` tag."""
        return "\n".join(
            f'<script src="{url}"></script>'
            for url in (self.tail_js_urls if urls is None else urls)
        )

    def get_head_js_str(self, urls: Sequence[str] | None = None) -> str:
        """Return the string of JavaScript URLs that should be loaded in the `<head>` tag."""
        return "\n".join(
            f'<script src="{url}"></script>'
            for url in (self.head_js_urls if urls is None else urls)
        )

    def get_head_css_str(self, urls: Sequence[str] | None = None) -> str:
        """Return the string of CSS URLs that should be loaded in the `<head>` tag."""
        return "\n".join(
            f'<link type="text/css" rel="stylesheet" href="{url}">'
            for url in (self.head_css_urls if urls is None else urls)
        )
