"""Smoke tests for openapipages package."""

import importlib.metadata

from openapipages.__about__ import __version__


def test_smoke() -> None:
    """Test that the package can be imported."""
    import openapipages  # noqa: PLC0415

    assert openapipages is not None
    assert __version__ == importlib.metadata.version("openapipages")
