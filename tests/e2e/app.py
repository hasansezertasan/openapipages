"""FastAPI app that serves every renderer against a real OpenAPI spec.

This module exposes a single module-level ``app`` that the uvicorn subprocess
fixture boots (see ``tests/e2e/conftest.py``). It is intentionally kept tiny and
dependency-light: FastAPI already ships with the project's test extras, and no
database or external service is involved.

The served spec carries a distinctive ``info.title`` (``API_TITLE``) that is
different from every page's HTML ``<title>``. Browser tests assert that
``API_TITLE`` appears in the rendered DOM, which can only happen once the UI's
JavaScript has booted, fetched ``/openapi.json``, parsed it, and rendered it.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from openapipages import Elements, RapiDoc, ReDoc, Scalar, SwaggerUI
from pydantic import BaseModel

API_TITLE = "OpenAPIPages E2E API"
"""``info.title`` of the served spec. Asserted to appear in the rendered DOM."""

E2E_SENTINEL = "openapipages-e2e-ok"
"""Body returned by ``/healthz`` — confirms the responding server is our app."""

OPENAPI_URL = "/openapi.json"
"""Where every renderer is pointed to load the spec from."""

RENDERER_PATHS = {
    "swaggerui": "/swaggerui",
    "redoc": "/redoc",
    "rapidoc": "/rapidoc",
    "elements": "/elements",
    "scalar": "/scalar",
}
"""Renderer name -> page path. Shared by the browser and HTTP e2e tests."""

# Built-in FastAPI docs are disabled so the only doc pages are the ones we mount
# below — nothing competes for the ``/redoc`` or ``/docs`` paths.
app = FastAPI(title=API_TITLE, version="1.0.0", docs_url=None, redoc_url=None)


class Widget(BaseModel):
    """A trivial model, present only to give the spec a schema to render."""

    id: int
    name: str


@app.get("/healthz", response_class=PlainTextResponse, include_in_schema=False)
def healthz() -> str:
    """Return the sentinel so the test fixture can verify it hit our server."""
    return E2E_SENTINEL


@app.get("/widgets", summary="List widgets", tags=["widgets"])
def list_widgets() -> list[Widget]:
    # A real operation so the rendered UIs have an endpoint to display.
    return [Widget(id=1, name="first")]


@app.get("/swaggerui", response_class=HTMLResponse, include_in_schema=False)
def get_swaggerui() -> str:
    return SwaggerUI(title="SwaggerUI", openapi_url=OPENAPI_URL).render()


@app.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
def get_redoc() -> str:
    return ReDoc(title="ReDoc", openapi_url=OPENAPI_URL).render()


@app.get("/rapidoc", response_class=HTMLResponse, include_in_schema=False)
def get_rapidoc() -> str:
    return RapiDoc(title="RapiDoc", openapi_url=OPENAPI_URL).render()


@app.get("/elements", response_class=HTMLResponse, include_in_schema=False)
def get_elements() -> str:
    return Elements(title="Elements", openapi_url=OPENAPI_URL).render()


@app.get("/scalar", response_class=HTMLResponse, include_in_schema=False)
def get_scalar() -> str:
    return Scalar(title="Scalar", openapi_url=OPENAPI_URL).render()
