from dataclasses import dataclass

from typing_extensions import Annotated, Doc

from .base import Base


@dataclass
class RapiDoc(Base):
    """Alternative API docs using RapiDoc."""

    js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the RapiDoc JavaScript.
            It is normally set to a CDN URL.
            """
        ),
    ] = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

    def render(self) -> str:
        """Generate and return the HTML response that loads RapiDoc for the alternative API docs."""
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
        html = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8"/>
                <title>{title}</title>
                <link rel="shortcut icon" href="{favicon_url}">
                {head_css_str}
                {head_js_str}
            </head>
            <body>
                <noscript>
                    RapiDoc requires Javascript to function. Please enable it to browse the documentation.
                </noscript>
                <rapi-doc spec-url="{openapi_url}"></rapi-doc>
                {tail_js_str}
            </body>
        </html>
        """
        return html
