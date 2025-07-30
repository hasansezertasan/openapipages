from typing import Dict

from openapipages import Elements, RapiDoc, ReDoc, Scalar, SwaggerUI

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Disable the built-in /redoc page so we can make a custom one.
app = FastAPI(redoc_url=None)


@app.get("/")
def root() -> Dict[str, str]:
    return {"Hello": "World"}


@app.get("/swaggerui", response_class=HTMLResponse, include_in_schema=False)
def get_swaggerui() -> str:
    return SwaggerUI(title="Swagger UI").render()


@app.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
def get_redoc() -> str:
    return ReDoc(title="ReDoc").render()


@app.get("/scalar", response_class=HTMLResponse, include_in_schema=False)
def get_scalar() -> str:
    return Scalar(title="Scalar").render()


@app.get("/elements", response_class=HTMLResponse, include_in_schema=False)
def get_elements() -> str:
    return Elements(title="Elements").render()


@app.get("/rapidoc", response_class=HTMLResponse, include_in_schema=False)
def get_rapidoc() -> str:
    return RapiDoc(title="RapiDoc").render()
