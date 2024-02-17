import json
from dataclasses import dataclass

from typing_extensions import Annotated, Any, Dict, Doc, Optional

from .base import Base

default_parameters: Annotated[
    Dict[str, Any],
    Doc(
        """
        Default configurations for Redoc UI.
        You can use it as a template to add any other configurations needed.
        Available options can be found here:
        https://github.com/Redocly/redoc/blob/main/docs/config.md#theme-settings
        """
    ),
] = {
    "theme": {
        "typography": {"code": {"wrap": True}},
    },
    "hide-download-button": False,
}


@dataclass
class ReDoc(Base):
    """Alternative API docs using ReDoc."""

    js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the ReDoc JavaScript.
            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    with_google_fonts: Annotated[
        bool,
        Doc(
            """
            Load and use Google Fonts.
            """
        ),
    ] = True
    ui_parameters: Annotated[
        Optional[Dict[str, Any]],
        Doc(
            """
            Configuration parameters for Redoc UI.
            It defaults to [redoc_ui_default_parameters][fastapi.openapi.docs.redoc_ui_default_parameters].
            """
        ),
    ] = None

    def render(self) -> str:
        """Generate and return the HTML response that loads ReDoc for the alternative API docs."""
        self.tail_js_urls.insert(0, self.js_url)
        google_fonts_str = ""
        if self.with_google_fonts:
            google_fonts_str = """<link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">"""

        current_redoc_ui_parameters = default_parameters.copy()
        current_redoc_ui_parameters.update(self.ui_parameters or {})

        def add_redoc_ui_parameters() -> str:
            _props = ""
            for key, value in current_redoc_ui_parameters.items():
                if value:
                    _props += f"{key}='{json.dumps(value)}' "
                else:
                    _props += f"{key} "
            return _props

        html_template = self.get_html_template()
        return html_template.format(
            title=self.title,
            favicon_url=self.favicon_url,
            openapi_url=self.openapi_url,
            head_css_str=self.get_head_css_str(),
            head_js_str=self.get_head_js_str(),
            tail_js_str=self.get_tail_js_str(),
            google_fonts_str=google_fonts_str,
            redoc_ui_parameters=add_redoc_ui_parameters(),
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
                {google_fonts_str}
                {head_css_str}
                {head_js_str}
                <!-- ReDoc doesn't change outer page styles -->
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                    }}
                </style>
            </head>
            <body>
                <noscript>
                    ReDoc requires Javascript to function. Please enable it to browse the documentation.
                </noscript>
                <redoc spec-url="{openapi_url}" {redoc_ui_parameters}></redoc>
                {tail_js_str}
            </body>
        </html>
        """
        return html
