# /// script
# requires-python = ">=3.8"
# dependencies = ["openapipages", "fastapi", "uvicorn"]
# [tool.uv.sources]
# openapipages = { path = "../../", editable = true }
# ///
# ruff: noqa: S104
from typing import Dict

import uvicorn
from openapipages import Elements, RapiDoc, ReDoc, Scalar, SwaggerUI

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Disable the built-in /redoc page so we can make a custom one.
app = FastAPI(redoc_url=None)


@app.get("/")
def root() -> Dict[str, str]:
    """Root of the application.

    Returns:
        dict: A dictionary with a greeting message.
    """
    return {"Hello": "World"}


@app.get("/swaggerui", response_class=HTMLResponse, include_in_schema=False)
def get_swaggerui() -> str:
    """Swagger UI.

    Returns:
        str: Rendered HTML for the Swagger UI page.
    """
    return SwaggerUI(title="Swagger UI").render()


@app.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
def get_redoc() -> str:
    """Redoc.

    Returns:
        str: Rendered HTML for the ReDoc page.
    """
    return ReDoc(title="ReDoc").render()


@app.get("/scalar", response_class=HTMLResponse, include_in_schema=False)
def get_scalar() -> str:
    """Scalar.

    Returns:
        str: Rendered HTML for the Scalar page.
    """
    return Scalar(title="Scalar").render()


@app.get("/elements", response_class=HTMLResponse, include_in_schema=False)
def get_elements() -> str:
    """Elements.

    Returns:
        str: Rendered HTML for the Elements page.
    """
    return Elements(title="Elements").render()


@app.get("/rapidoc", response_class=HTMLResponse, include_in_schema=False)
def get_rapidoc() -> str:
    """RapiDoc.

    Returns:
        str: Rendered HTML for the RapiDoc page.
    """
    return RapiDoc(title="RapiDoc").render()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
