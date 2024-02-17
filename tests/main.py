from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openapipages import Elements, RapiDoc, ReDoc, Scalar, SwaggerUI
from typing_extensions import Dict

app = FastAPI()


@app.get("/")
def root() -> Dict[str, str]:
    return {"Hello": "World"}


@app.get("/swaggerui-plain", response_class=HTMLResponse, include_in_schema=False)
def get_swaggerui_plain() -> str:
    return SwaggerUI(title="Swagger UI").render()


@app.get("/swaggerui-custom", response_class=HTMLResponse, include_in_schema=False)
def get_swaggerui_custom() -> str:
    return SwaggerUI(
        title="Swagger UI",
        js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
        init_oauth={
            "clientId": "the-application-clients",
            "appName": "Test Application",
        },
        oauth2_redirect_url=None,
        swagger_ui_parameters={
            "syntaxHighlight": False,
            "syntaxHighlight.theme": "obsidian",
            "deepLinking": False,
        },
    ).render()


@app.get("/redoc-plain", response_class=HTMLResponse, include_in_schema=False)
def get_redoc_plain() -> str:
    return ReDoc(title="ReDoc").render()


@app.get("/redoc-custom", response_class=HTMLResponse, include_in_schema=False)
def get_redoc_custom() -> str:
    return ReDoc(
        title="ReDoc", js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js"
    ).render()


@app.get("/scalar-plain", response_class=HTMLResponse, include_in_schema=False)
def get_scalar_plain() -> str:
    return Scalar(title="Scalar").render()


@app.get("/scalar-custom", response_class=HTMLResponse, include_in_schema=False)
def get_scalar_custom() -> str:
    return Scalar(
        title="Scalar",
        js_url="https://cdn.jsdelivr.net/npm/@scalar/api-reference",
    ).render()


@app.get("/elements", response_class=HTMLResponse, include_in_schema=False)
def get_elements() -> str:
    return Elements(title="Elements").render()


@app.get("/rapidoc", response_class=HTMLResponse, include_in_schema=False)
def get_rapidoc() -> str:
    return RapiDoc(title="RapiDoc").render()
