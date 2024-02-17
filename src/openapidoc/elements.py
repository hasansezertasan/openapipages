from dataclasses import dataclass

from typing_extensions import Annotated, Doc

from .base import Base


@dataclass
class Elements(Base):
    """Alternative API docs using Stoplight Elements."""

    js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Stoplight Elements JavaScript.
            It is normally set to a CDN URL.
            """
        ),
    ] = "https://unpkg.com/@stoplight/elements/web-components.min.js"
    css_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Stoplight Elements CSS.
            It is normally set to a CDN URL.
            """
        ),
    ] = "https://unpkg.com/@stoplight/elements/styles.min.css"

    def render(self) -> str:
        """Generate and return the HTML response that loads Stoplight Elements for the alternative API docs."""
        self.head_css_urls.insert(0, self.css_url)
        self.head_js_urls.insert(0, self.js_url)
        html_template = self.get_html_template()
        return html_template.format(
            title=self.title,
            favicon_url=self.favicon_url,
            openapi_url=self.openapi_url,
            head_css_str=self.get_head_css_str(),
            head_js_str=self.get_head_js_str(),
            tail_js_str=self.get_tail_js_str(),
        )

    def get_html_template(self) -> str:
        html = """<!doctype html>
        <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <title>{title}</title>
                <link rel="shortcut icon" href="{favicon_url}">
                {head_css_str}
                {head_js_str}
            </head>
            <body>
                <noscript>
                    Stoplight Elements requires Javascript to function. Please enable it to browse the documentation.
                </noscript>
                <elements-api apiDescriptionUrl="{openapi_url}" router="hash" layout="sidebar"/>
                {tail_js_str}
            </body>
        </html>"""
        return html
