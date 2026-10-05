"""Smoke tests for openapipages package."""


def test_smoke() -> None:
    """Test that the package can be imported."""
    import openapipages  # noqa: PLC0415

    assert openapipages is not None
