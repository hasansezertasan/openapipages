from dataclasses import dataclass, field

from typing_extensions import Annotated, Doc, List


@dataclass
class Base:
    """Base class for alternative API docs."""

    title: Annotated[
        str,
        Doc(
            """
            The HTML `<title>` content, normally shown in the browser tab.
            """
        ),
    ]
    js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the JavaScript.
            It is normally set to a CDN URL.
            """
        ),
    ]
    openapi_url: Annotated[
        str,
        Doc(
            """
            The OpenAPI URL that page should load and use.
            Default URL `/openapi.json`.
            """
        ),
    ] = "/openapi.json"
    head_js_urls: Annotated[
        List[str],
        Doc(
            """
            A list of URLs to JavaScript files that should be loaded in the `<head>` tag.
            """
        ),
    ] = field(default_factory=list)
    tail_js_urls: Annotated[
        List[str],
        Doc(
            """
            A list of URLs to JavaScript files that should be loaded at the end of the `<body>` tag.
            """
        ),
    ] = field(default_factory=list)
    head_css_urls: Annotated[
        List[str],
        Doc(
            """
            A list of URLs to CSS files that should be loaded in the `<head>` tag.
            """
        ),
    ] = field(default_factory=list)
    favicon_url: Annotated[
        str,
        Doc(
            """
            The URL of the favicon to use. It is normally shown in the browser tab.
            """
        ),
    ] = "/favicon.ico"

    def render(self) -> str:
        """Generate and return the HTML response that leads page for alternative API docs."""
        html_template = self.get_html_template()
        return html_template.format(
            title=self.title,
            favicon_url=self.favicon_url,
            head_css_str=self.get_head_css_str(),
            head_js_str=self.get_head_js_str(),
            tail_js_str=self.get_tail_js_str(),
        )

    def get_html_template(self) -> str:
        """Return the HTML template for the alternative API docs."""
        html = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>{title}</title>
                <link rel="shortcut icon" href="{favicon_url}">
                {head_css_str}
                {head_js_str}
            </head>
            <body>
                {tail_js_str}
            </body>
        </html>
        """
        return html

    def get_tail_js_str(self) -> str:
        """Return the string of JavaScript URLs that should be loaded at the end of the `<body>` tag."""
        string = "\n".join(
            [f'<script src="{url}"></script>' for url in self.tail_js_urls]
        )
        return string

    def get_head_js_str(self) -> str:
        """Return the string of JavaScript URLs that should be loaded in the `<head>` tag."""
        if self.head_js_urls:
            string = "\n".join(
                [f'<script src="{url}"></script>' for url in self.head_js_urls]
            )
        else:
            string = ""
        return string

    def get_head_css_str(self) -> str:
        """Return the string of CSS URLs that should be loaded in the `<head>` tag."""
        if self.head_css_urls:
            string = "\n".join(
                [
                    f'<link type="text/css" rel="stylesheet"  href="{url}">'
                    for url in self.head_css_urls
                ]
            )
        else:
            string = ""
        return string
