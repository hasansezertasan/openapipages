"""E2E fixtures: a subprocess uvicorn server plus an auto ``e2e`` marker.

Adapted from the pattern in ``starlette-admin-fields``: boot the real ASGI app
in a subprocess on a free port, wait until a ``/healthz`` sentinel confirms it is
ready, then hand tests a ``base_url`` for ``page.goto(...)``.
"""

from __future__ import annotations

import contextlib
import pathlib
import socket
import subprocess  # nosec B404
import sys
import time
import warnings
from typing import TYPE_CHECKING

import httpx
import pytest

from tests.e2e.app import E2E_SENTINEL

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import Any

    from playwright.sync_api import Browser, Page

SERVER_READY_TIMEOUT_S = 30.0
SERVER_POLL_INTERVAL_S = 0.2
SERVER_SHUTDOWN_TIMEOUT_S = 5.0

E2E_DIR = pathlib.Path(__file__).parent.resolve()

# 0 = clean exit; SIGTERM (-15) = normal shutdown; SIGKILL (-9) = forced kill
# when the graceful shutdown timeout expires in teardown.
_ACCEPTABLE_RETURNCODES = {0, -15, -9}


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Auto-mark every test under ``tests/e2e/`` with ``@pytest.mark.e2e``."""
    e2e_marker = pytest.mark.e2e
    for item in items:
        if item.path.is_relative_to(E2E_DIR):
            item.add_marker(e2e_marker)


@pytest.fixture(scope="session")
def free_port() -> int:
    """Bind to port 0 then release it — race-safe enough for local + CI.

    Returns:
        int: A port number that was free at the moment of binding.
    """
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@pytest.fixture(scope="session")
def uvicorn_server(free_port: int) -> Iterator[str]:
    """Boot ``tests.e2e.app:app`` under uvicorn in a subprocess.

    Tears down with terminate -> kill. stdout and stderr are merged into a single
    pipe so any startup errors appear in failure messages.

    Yields:
        str: The base URL (``http://127.0.0.1:<port>``) the server is listening on.

    Raises:
        RuntimeError: If the server exits early or never becomes ready in time.
    """
    proc = subprocess.Popen(  # nosec B603
        [
            sys.executable,
            "-m",
            "uvicorn",
            "tests.e2e.app:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(free_port),
            "--log-level",
            "warning",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    # PIPE is set above, so stdout is guaranteed present; bind a narrowed local
    # so both mypy and basedpyright accept the .read() calls below.
    proc_stdout = proc.stdout
    assert proc_stdout is not None

    base_url = f"http://127.0.0.1:{free_port}"
    deadline = time.monotonic() + SERVER_READY_TIMEOUT_S
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            output = proc_stdout.read().decode(errors="replace")
            msg = (
                f"uvicorn exited prematurely (returncode={proc.returncode}) "
                f"at {base_url}.\noutput: {output}"
            )
            raise RuntimeError(msg)
        try:
            response = httpx.get(f"{base_url}/healthz", timeout=1.0)
        except (httpx.ConnectError, httpx.TimeoutException):
            # Server not accepting connections yet — normal during startup.
            time.sleep(SERVER_POLL_INTERVAL_S)
            continue
        except (httpx.ReadError, httpx.WriteError, httpx.RemoteProtocolError):
            # Connection accepted but then dropped — check if the process died.
            if proc.poll() is not None:
                output = proc_stdout.read().decode(errors="replace")
                msg = (
                    f"uvicorn died mid-request (returncode={proc.returncode}) "
                    f"at {base_url}.\noutput: {output}"
                )
                raise RuntimeError(msg) from None
            time.sleep(SERVER_POLL_INTERVAL_S)
            continue
        if response.status_code == httpx.codes.OK and response.text == E2E_SENTINEL:
            # Sentinel check confirms the responding server is our test app,
            # not an unrelated process that happened to grab the same port.
            break
        time.sleep(SERVER_POLL_INTERVAL_S)
    else:
        proc.kill()
        output_bytes, _ = proc.communicate()
        output = output_bytes.decode(errors="replace")
        msg = (
            f"uvicorn did not become ready at {base_url} "
            f"within {SERVER_READY_TIMEOUT_S}s.\noutput: {output}"
        )
        raise RuntimeError(msg)

    try:
        yield base_url
    finally:
        proc.terminate()
        try:
            output_bytes, _ = proc.communicate(timeout=SERVER_SHUTDOWN_TIMEOUT_S)
        except subprocess.TimeoutExpired:
            proc.kill()
            output_bytes, _ = proc.communicate()
        if proc.returncode not in _ACCEPTABLE_RETURNCODES:
            output_tail = output_bytes.decode(errors="replace")[-2000:]
            msg = (
                f"uvicorn exited with unexpected code {proc.returncode}:\n{output_tail}"
            )
            # If a test already failed, warn instead of masking that exception.
            if sys.exc_info()[1] is None:
                pytest.fail(msg)
            else:
                warnings.warn(msg, stacklevel=1)


@pytest.fixture(scope="session")
def base_url(uvicorn_server: str) -> str:
    """Alias used by ``page.goto`` callers.

    Returns:
        str: The base URL of the running server.
    """
    return uvicorn_server


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict[str, Any],
) -> dict[str, Any]:
    """Override pytest-playwright's launch args to stabilise Chromium in CI.

    ``--disable-dev-shm-usage`` avoids crashes on containers with a tiny
    ``/dev/shm`` (common on CI runners and in Docker). Idea borrowed from
    ``xgovuk-flask-admin``.

    Returns:
        dict[str, Any]: The launch args with the extra flag appended.
    """
    return {**browser_type_launch_args, "args": ["--disable-dev-shm-usage"]}


@pytest.fixture
def no_js_page(browser: Browser) -> Iterator[Page]:
    """Yield a page in a context with JavaScript disabled.

    Used to verify the ``<noscript>`` fallbacks — a browser only renders
    ``<noscript>`` contents when scripting is off.

    Yields:
        Page: A Playwright page that will not execute page scripts.
    """
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    try:
        yield page
    finally:
        context.close()
