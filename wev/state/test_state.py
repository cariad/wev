from mock import Mock, patch

from wev.state import State


def test() -> None:
    assert State()


@patch("wev.state.state.ResolutionCache")
def test_resolution_cache(resolution_cache: Mock) -> None:
    state = State()
    state.resolution_cache
    state.resolution_cache
    resolution_cache.assert_called_once()
