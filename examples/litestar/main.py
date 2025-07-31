# ruff: noqa: RUF029, S104
from __future__ import annotations

from typing import Any, Dict

import uvicorn
from litestar import Litestar, MediaType, get
from openapipages import Elements, RapiDoc, ReDoc, Scalar, SwaggerUI

from litestar import Litestar, MediaType, get

openapi_url = "/schema/openapi.json"


@get("/")
async def root() -> Dict[str, Any]:
    return {"Hello": "World"}


@get("/swaggerui", media_type=MediaType.HTML, include_in_schema=False)
async def get_swaggerui() -> str:
    return SwaggerUI(title="Swagger UI", openapi_url=openapi_url).render()


@get("/redoc", media_type=MediaType.HTML, include_in_schema=False)
async def get_redoc() -> str:
    return ReDoc(title="ReDoc", openapi_url=openapi_url).render()


@get("/scalar", media_type=MediaType.HTML, include_in_schema=False)
async def get_scalar() -> str:
    return Scalar(title="Scalar", openapi_url=openapi_url).render()


@get("/elements", media_type=MediaType.HTML, include_in_schema=False)
async def get_elements() -> str:
    return Elements(title="Elements", openapi_url=openapi_url).render()


@get("/rapidoc", media_type=MediaType.HTML, include_in_schema=False)
async def get_rapidoc() -> str:
    return RapiDoc(title="RapiDoc", openapi_url=openapi_url).render()


app = Litestar([root, get_swaggerui, get_redoc, get_scalar, get_elements, get_rapidoc])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
