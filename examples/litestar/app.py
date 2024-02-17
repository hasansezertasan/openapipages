from litestar import Litestar, MediaType, get
from openapipages import Elements, RapiDoc, ReDoc, Scalar, SwaggerUI

openapi_url = "/schema/openapi.json"


@get("/")
def root() -> dict[str, str]:
    return {"Hello": "World"}


@get("/swaggerui", media_type=MediaType.HTML, include_in_schema=False)
def get_swaggerui() -> str:
    return SwaggerUI(title="Swagger UI", openapi_url=openapi_url).render()


@get("/redoc", media_type=MediaType.HTML, include_in_schema=False)
def get_redoc() -> str:
    return ReDoc(title="ReDoc", openapi_url=openapi_url).render()


@get("/scalar", media_type=MediaType.HTML, include_in_schema=False)
def get_scalar() -> str:
    return Scalar(title="Scalar", openapi_url=openapi_url).render()


@get("/elements", media_type=MediaType.HTML, include_in_schema=False)
def get_elements() -> str:
    return Elements(title="Elements", openapi_url=openapi_url).render()


@get("/rapidoc", media_type=MediaType.HTML, include_in_schema=False)
def get_rapidoc() -> str:
    return RapiDoc(title="RapiDoc", openapi_url=openapi_url).render()


app = Litestar([root, get_swaggerui, get_redoc, get_scalar, get_elements, get_rapidoc])
