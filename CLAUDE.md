# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`openapipages` is a zero-dependency, framework-agnostic Python library that renders HTML pages for OpenAPI documentation UIs: SwaggerUI, ReDoc, RapiDoc, Elements, and Scalar. It does **not** generate the OpenAPI spec — it only renders pages that point at one.

Supports Python 3.10+ (project pins `requires-python = ">=3.10"`; mypy targets 3.10; ruff targets py310).

## Commands

The project uses **Hatch** (with `uv` as installer) for env management. Most workflows go through `hatch`.

```bash
# Install/sync everything (Hatch resolves the test env on first use)
hatch env create test

# Run the full test matrix on the default Python
hatch run test:test

# Coverage report (after running tests)
hatch run test:cov

# Style + static analysis (codespell, validate-pyproject, ruff check/format, mypy)
hatch run test:style

# Run pre-commit on all files
hatch run pre

# A single test file or test
hatch run test:python -m pytest tests/integration/test_swaggerui.py
hatch run test:python -m pytest tests/integration/test_swaggerui.py::test_name -v
```

The test matrix (`[[tool.hatch.envs.test.matrix]]`) covers Python 3.10–3.14; CI runs across these.

Coverage `fail_under = 99` — coverage gaps will fail the build.

## Architecture

All five doc renderers inherit from `Base` (`src/openapipages/base.py`), a `@dataclass` that:

1. Holds shared config: `title`, `js_url`, `openapi_url`, `head_js_urls`, `tail_js_urls`, `head_css_urls`, `favicon_url`.
2. Exposes `render()` which formats `get_html_template()` with `{title}`, `{favicon_url}`, `{head_css_str}`, `{head_js_str}`, `{tail_js_str}`.
3. Each subclass (`swaggerui.py`, `redoc.py`, `rapidoc.py`, `elements.py`, `scalar.py`) overrides `get_html_template()` and may add UI-specific fields (e.g. SwaggerUI exposes `init_oauth`, `swagger_ui_parameters`, `oauth2_redirect_url`).

The public API is just the five classes re-exported from `openapipages/__init__.py`. Consumers call `Renderer(title=...).render()` and return the resulting string as an HTML response in whatever framework they're using.

Fields use `Annotated[..., Doc(...)]` for inline documentation — `Annotated` comes from stdlib `typing` (py310+), `Doc` from `typing_extensions` (PEP 727 was withdrawn, so it lives there permanently). Preserve that split when adding new options.

`tests/main.py` is a FastAPI app that exercises every renderer (plain + custom variants). The per-renderer test files spin it up via `httpx`/`fastapi.testclient` and assert on rendered HTML.

## Conventions

- **Conventional Commits** for commit messages and **Conventional Branch** for branch names (enforced via `.pre-commit-config.yaml` / repo policy).
- Ruff is configured with `select = ["ALL"]` and `preview = true`; relative imports are banned (`ban-relative-imports = "all"`) — always import from `openapipages.<module>`.
- `mypy --strict` is enforced over `src/`. Keep everything fully typed.
- Examples in `examples/fastapi` and `examples/litestar` should stay runnable; if you change the public API, update them.
