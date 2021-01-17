from wev.version import get_version


def test_get_version() -> None:
    assert len(get_version()) > 3
