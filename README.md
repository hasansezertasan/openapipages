# Open API Pages

[![PyPI - Version](https://img.shields.io/pypi/v/openapipages.svg)](https://pypi.org/project/openapipages)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openapipages.svg)](https://pypi.org/project/openapipages)
[![License](https://img.shields.io/github/license/hasansezertasan/openapipages.svg)](https://github.com/hasansezertasan/openapipages/blob/main/LICENSE)
[![Latest Commit](https://img.shields.io/github/last-commit/hasansezertasan/openapipages)](https://github.com/hasansezertasan/openapipages)

[![Downloads](https://pepy.tech/badge/openapipages)](https://pepy.tech/project/openapipages)
[![Downloads/Month](https://pepy.tech/badge/openapipages/month)](https://pepy.tech/project/openapipages)
[![Downloads/Week](https://pepy.tech/badge/openapipages/week)](https://pepy.tech/project/openapipages)

Totally Pythonic, OpenAPI Based customizable documentation pages for [SwaggerUI], [ReDoc], [RapiDoc], [Elements], [Scalar].

> Keep in mind, that this package doesn't generate [OpenAPI] Spec, it just renders the pages with the given configuration.

---

## Table of Contents

- [Open API Pages](#open-api-pages)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
    - [Progress](#progress)
  - [Installation](#installation)
  - [Usage](#usage)
    - [FastAPI](#fastapi)
    - [Litestar](#litestar)
  - [Motivation](#motivation)
    - [Developer Experience](#developer-experience)
    - [Configuration](#configuration)
    - [Alternatives](#alternatives)
    - [Standardisation](#standardisation)
  - [See Also](#see-also)
    - [Projects](#projects)
    - [Issues, PRs, and Discussions](#issues-prs-and-discussions)
  - [Author](#author)
  - [Disclaimer](#disclaimer)
  - [License](#license)

## Features

> Gimme an OpenAPI Spec, leave the rest to me...

- Framework agnostic.
- Zero dependencies, just Python standard library.
- Fully typed.
- Highly extensible.

### Progress

| Documentation | Page               | Config             |
| ------------- | ------------------ | ------------------ |
| [SwaggerUI]   | :white_check_mark: | :heavy_check_mark: |
| [ReDoc]       | :white_check_mark: | :heavy_check_mark: |
| [RapiDoc]     | :white_check_mark: | :heavy_check_mark: |
| [Elements]    | :white_check_mark: | :heavy_check_mark: |
| [Scalar]      | :white_check_mark: | :heavy_check_mark: |

Emoji Key:

| Emoji                 | Meaning     |
| --------------------- | ----------- |
| :white_check_mark:    | Ready       |
| :heavy_check_mark:    | Partially   |
| :x:                   | Failed      |
| :construction:        | In Progress |
| :white_square_button: | Pending     |
| :warning:             | Not sure    |

## Installation

```console
pip install openapipages
```

## Usage

I know it looks a bit boilerplate but it's all straight-forward. The `.render()` method returns the HTML as a string. Thanks to this design, you can extend and configure the pages as you wish (e.g. add extra logic to restrict access to the page).

### FastAPI

> The `include_in_schema` parameter is set to `False` in each endpoint to avoid including these endpoints in the OpenAPI Spec.

```python
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from openapipages import Elements, RapiDoc, ReDoc, Scalar, SwaggerUI

app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
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

```

### Litestar

> The `include_in_schema` parameter is set to `False` in each endpoint to avoid including these endpoints in the OpenAPI Spec.

```python
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

```

## Motivation

TL;DR - I don't want to copy and paste it again...

### Developer Experience

Several API Documentation tools are ready to use at your fingertips with a standard interface.

No more copying and pasting the same thing from one project to another. Import the package and use it!

### Configuration

Here is a pull request made to the [FastAPI] repo. This was the point I understood the configuration was limited and it wouldn't change...

- [Allow passing ui parameters to redoc html by adriantre · Pull Request #10437 · tangelo/fastapi](https://github.com/tiangolo/fastapi/pull/10437)

Also, the author's answer to this PR shows that we won't be seeing more alternative documentation tools in the future.

### Alternatives

Here is another pull request made to the [FastAPI] repo. It brings [Scalar] support, but it's not approved/merged yet and we think it will stay that way thanks to the previous PR.

- [feat: add scalar integration (additional alternative to Swagger UI/Redoc) by marclave · Pull Request #10674 · tiangolo/fastapi](https://github.com/tiangolo/fastapi/pull/10674)

### Standardisation

> A standard interface for many API Documentation Interfaces with configuration features.

Lately, OpenAPI Spec-based Documentation tools have become popular in the Python community. We see a lot of projects ([FastAPI], [Litestar], [APISpec], [flasgger], [SpecTree], [Connexion], etc) offering support for OpenAPI Specification out of the box.

[Litestar] has support for [SwaggerUI], [ReDoc], [RapiDoc], and [Elements] and [FastAPI] has support for [SwaggerUI], and [ReDoc] but what is next? Will the next one be enough?

They all have one thing in common, some HTML (as Python string or a file) templated with the given configuration.

Do you see where I am going?

I want `openapipages` to be SQLAlchemy of OpenAPI Spec-based Documentation tools.

One interface for many! And of course Framework agnostic... So you can use it in your [FastAPI], [Litestar] projects, or any other project that generates OpenAPI specifications.

## See Also

### Projects

- [kemingy/defspec: Create the OpenAPI spec and document from dataclass, attrs, etc.](https://github.com/kemingy/defspec/)
- [spec-first/swagger_ui_bundle: bundled swagger-ui pip package](https://github.com/spec-first/swagger_ui_bundle)
- [spec-first/connexion: Connexion is a modern Python web framework that makes spec-first and api-first development easy.][Connexion]
- [sveint/flask-swagger-ui: Swagger UI blueprint for flask](https://github.com/sveint/flask-swagger-ui)
- [flasgger/flasgger: Easy OpenAPI specs and Swagger UI for your Flask API][flasgger]
- [marshmallow-code/apispec: A pluggable API specification generator. Currently supports the OpenAPI Specification (f.k.a. the Swagger specification)..][APISpec]
- [jmcarp/flask-apispec][Flask-apispec]

### Issues, PRs, and Discussions

- [[Question] Is it possible to load the Swagger UI offline? · Issue #261 · 0b01001001/spectree](https://github.com/0b01001001/spectree/issues/261)
- [Swagger with hosted files does not work after upgrade · tiangolo/fastapi · Discussion #10426](https://github.com/tiangolo/fastapi/discussions/10426)
- [♻️ Generate cleaner Swagger HTML by s-rigaud · Pull Request #11072 · tiangolo/fastapi](https://github.com/tiangolo/fastapi/pull/11072)

## Author

- [Hasan Sezer Tasan](https://www.github.com/hasansezertasan), It's me :wave:

## Disclaimer

[FastAPI] and [Litestar] projects and the two pull requests mentioned above inspired me to create this package.

## License

`openapipages` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

<!-- Links -->
[OpenAPI]: https://github.com/OAI/OpenAPI-Specification
<!-- Python Projects -->
[FastAPI]: https://github.com/tiangolo/fastapi
[Litestar]: https://github.com/litestar-org/litestar
[SpecTree]: https://github.com/0b01001001/spectree
[flasgger]: https://github.com/flasgger/flasgger
[Connexion]: https://github.com/spec-first/connexion
[APISpec]: https://github.com/marshmallow-code/apispec
[Flask-apispec]: https://github.com/jmcarp/flask-apispec
<!-- API Documentation Tools -->
[Scalar]: https://github.com/scalar/scalar
[Elements]: https://github.com/stoplightio/elements
[RapiDoc]: https://github.com/rapi-doc/RapiDoc
[ReDoc]: https://github.com/Redocly/redoc
[SwaggerUI]: https://github.com/swagger-api/swagger-ui
