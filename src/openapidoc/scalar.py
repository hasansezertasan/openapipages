from dataclasses import dataclass

from typing_extensions import Annotated, Doc

from .base import Base


@dataclass
class Scalar(Base):
    """Alternative API docs using Scalar."""

    js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Scalar JavaScript.
            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/@scalar/api-reference"
    proxy_url: Annotated[
        str,
        Doc(
            """
            The URL to use to set the Scalar Proxy.
            It is normally set to a Scalar API URL (https://api.scalar.com/request-proxy), but default is empty.
            """
        ),
    ] = ""

    def render(self) -> str:
        """Generate and return the HTML response that loads Scalar for the alternative API docs."""
        self.tail_js_urls.insert(0, self.js_url)
        html_template = self.get_html_template()
        return html_template.format(
            title=self.title,
            favicon_url=self.favicon_url,
            openapi_url=self.openapi_url,
            proxy_url=self.proxy_url,
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
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>{title}</title>
                <link rel="shortcut icon" href="{favicon_url}">
                {head_css_str}
                {head_js_str}
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                    }}
                </style>
            </head>
            <body>
                <noscript>
                    Scalar requires Javascript to function. Please enable it to browse the documentation.
                </noscript>
                <script id="api-reference" data-url="{openapi_url}" data-proxy-url="{proxy_url}"></script>
                {tail_js_str}
            </body>
        </html>
        """
        return html
