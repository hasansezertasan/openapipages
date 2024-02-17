import json
from dataclasses import dataclass

from typing_extensions import Annotated, Any, Dict, Doc, List, Optional

from .base import Base

default_parameters: Annotated[
    Dict[str, Any],
    Doc(
        """
        Default configurations for Swagger UI.
        You can use it as a template to add any other configurations needed.
        """
    ),
] = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}
default_parameters_presets: Annotated[
    List[str],
    Doc(
        """
        Default configurations for Swagger UI presets.
        You can use it as a template to add any other configurations needed.
        """
    ),
] = ["SwaggerUIBundle.presets.apis", "SwaggerUIBundle.SwaggerUIStandalonePreset"]


@dataclass
class SwaggerUI(Base):
    """Alternative API docs using Swagger UI."""

    js_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI JavaScript.
            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"
    css_url: Annotated[
        str,
        Doc(
            """
            The URL to use to load the Swagger UI CSS.
            It is normally set to a CDN URL.
            """
        ),
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css"
    oauth2_redirect_url: Annotated[
        Optional[str],
        Doc(
            """
            The OAuth2 redirect URL.
            """
        ),
    ] = "/docs/oauth2-redirect"
    init_oauth: Annotated[
        Optional[Dict[str, Any]],
        Doc(
            """
            A dictionary with Swagger UI OAuth2 initialization configurations.
            """
        ),
    ] = None
    swagger_ui_parameters: Annotated[
        Optional[Dict[str, Any]],
        Doc(
            """
            Configuration parameters for Swagger UI.
            It defaults to [default_parameters][openapipages.swaggerui.default_parameters].
            """
        ),
    ] = None
    swagger_ui_presets: Annotated[
        Optional[List[str]],
        Doc(
            """
            Configuration parameters for Swagger UI presets.
            It defaults to [default_parameters][openapipages.swaggerui.default_parameters].
            """
        ),
    ] = None

    def render(self) -> str:
        """Generate and return the HTML that loads Swagger UI for the alternative API docs."""
        self.head_css_urls.insert(0, self.css_url)
        self.tail_js_urls.insert(0, self.js_url)
        current_swagger_ui_parameters = default_parameters.copy()
        current_swagger_ui_parameters.update({"url": self.openapi_url})
        if self.swagger_ui_parameters:
            current_swagger_ui_parameters.update(self.swagger_ui_parameters)
        current_swagger_ui_presets = default_parameters_presets.copy()
        if self.swagger_ui_presets:
            current_swagger_ui_presets.extend(self.swagger_ui_presets)
        presets = ", ".join(current_swagger_ui_presets)
        html_swagger_ui_parameters = "".join(
            [
                f"{json.dumps(key)}: {json.dumps(value)},"
                for key, value in current_swagger_ui_parameters.items()
            ]
        )
        html_oauth2_redirect_url = (
            f"oauth2RedirectUrl: window.location.origin + '{self.oauth2_redirect_url}',"
            if self.oauth2_redirect_url
            else ""
        )
        init_oauth_html = (
            f"ui.initOAuth({json.dumps(self.init_oauth)})" if self.init_oauth else ""
        )
        html_template = self.get_html_template()
        return html_template.format(
            title=self.title,
            favicon_url=self.favicon_url,
            head_css_str=self.get_head_css_str(),
            head_js_str=self.get_head_js_str(),
            tail_js_str=self.get_tail_js_str(),
            html_swagger_ui_parameters=html_swagger_ui_parameters,
            html_oauth2_redirect_url=html_oauth2_redirect_url,
            presets=presets,
            init_oauth_html=init_oauth_html,
        )

    def get_html_template(self) -> str:
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
                <div id="swagger-ui"></div>
                {tail_js_str}
                <!-- `SwaggerUIBundle` is now available on the page -->
                <script>
                    const ui = SwaggerUIBundle({{
                        {html_swagger_ui_parameters}
                        {html_oauth2_redirect_url}
                        presets: [{presets}],
                    }})
                    {init_oauth_html}
                </script>
            </body>
        </html>
        """
        return html
