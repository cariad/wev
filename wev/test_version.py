from wev.version import get_version


def test_get_version() -> None:
    assert get_version()
