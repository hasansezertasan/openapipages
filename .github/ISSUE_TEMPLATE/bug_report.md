---
name: Bug report
about: Report a bug in openapipages
title: 'Bug: '
labels: bug
assignees: 'hasansezertasan'

---
## Bug Description

<!--
This issue tracker is a tool to address bugs in openapipages itself.
Please use GitHub Discussions for questions about your own code.

Replace this comment with a clear outline of what the bug is.
-->

## How to Reproduce

<!--
Describe how to replicate the bug.

Please provide a minimal reproducible example that developers can run to investigate the problem.
You can find help for creating such an example [here](https://stackoverflow.com/help/minimal-reproducible-example).

Here is an example of a minimal reproducible example:

```python
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openapipages==0.1.0",
#     "fastapi",
#     "uvicorn",
# ]
# ///
from typing import Dict

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from openapipages import ReDoc

app = FastAPI(redoc_url=None)


@app.get("/")
def root() -> Dict[str, str]:
    """Root of the application."""
    return {"Hello": "World"}


@app.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
def get_redoc() -> str:
    """Redoc."""
    0/0  # This will raise a ZeroDivisionError
    return ReDoc(title="ReDoc").render()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Include the full traceback if there was an exception. For example:

```shell
INFO:     Started server process [19961]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:56096 - "GET /redoc HTTP/1.1" 500 Internal Server Error
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/uvicorn/protocols/http/h11_impl.py", line 403, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/fastapi/applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/applications.py", line 112, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/middleware/errors.py", line 187, in __call__
    raise exc
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/middleware/errors.py", line 165, in __call__
    await self.app(scope, receive, _send)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/middleware/exceptions.py", line 62, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/routing.py", line 715, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/routing.py", line 735, in app
    await route.handle(scope, receive, send)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/routing.py", line 288, in handle
    await self.app(scope, receive, send)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/routing.py", line 76, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/routing.py", line 73, in app
    response = await f(request)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/fastapi/routing.py", line 302, in app
    raw_response = await run_endpoint_function(
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/fastapi/routing.py", line 215, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/starlette/concurrency.py", line 37, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/anyio/to_thread.py", line 56, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/anyio/_backends/_asyncio.py", line 2364, in run_sync_in_worker_thread
    return await future
  File "/Users/hasansezertasan/openapipages/.venv/lib/python3.8/site-packages/anyio/_backends/_asyncio.py", line 864, in run
    result = context.run(func, *args)
  File "main.py", line 28, in get_redoc
    0/0
ZeroDivisionError: division by zero
```
-->

## Expected Behavior

<!--
Describe the expected behavior that should have happened but didn't.
-->

## Environment

<!--
You can skip this section if you have provided a minimal reproducible example that includes the
environment information as part of the code snippet (inline metadata).

Otherwise, please complete the following information

Read more about inline metadata:
  - [PEP 723 – Inline script metadata | peps.python.org](https://peps.python.org/pep-0723/)
  - [Inline script metadata - Python Packaging User Guide](https://packaging.python.org/en/latest/specifications/inline-script-metadata/)
-->

- openapipages version: [e.g. 0.1.0]
- Backend: [FastAPI, Starlette, ...]

### Additional Context

<!--
Add any other context about the problem here.
-->
