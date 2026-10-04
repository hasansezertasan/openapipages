from dataclasses import dataclass
from typing import Annotated

from openapipages.base import Base
from typing_extensions import Doc


@dataclass
class RapiDoc(Base):
    """Alternative API docs using RapiDoc."""

    js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the RapiDoc JavaScript.
            It is normally set to a CDN URL.
            """,
        ),
    ] = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

    def render(self) -> str:
        """Generate and return the HTML response that loads RapiDoc for the alternative API docs.

        Returns:
            str: The HTML response as a string that loads RapiDoc for the alternative API docs.
        """
        html_template = self.get_html_template()
        return html_template.format(
            title=self.title,
            favicon_url=self.favicon_url,
            openapi_url=self.openapi_url,
            head_css_str=self.get_head_css_str(),
            # Modules and deferred classic scripts execute in document order.
            head_js_str="\n".join(
                f'<script defer src="{url}"></script>' for url in self.head_js_urls
            ),
            js_url=self.js_url,
            tail_js_str="\n".join(
                f'<script defer src="{url}"></script>' for url in self.tail_js_urls
            ),
        )

    def get_html_template(self) -> str:
        """Return the RapiDoc page template with its module script."""
        return """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8"/>
                <title>{title}</title>
                <link rel="shortcut icon" href="{favicon_url}">
                {head_css_str}
                <script type="module" src="{js_url}"></script>
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
