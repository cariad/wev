from datetime import datetime, timedelta
from typing import Iterator, Optional

from mock import Mock, patch
from pytest import fixture, mark, raises

from wev.mock_plugin import MockPlugin
from wev.resolver import fresh_resolution, resolve
from wev.sdk import PluginBase, Resolution
from wev.sdk.exceptions import CannotResolveError
from wev.state import MockState


@fixture
def get_plugin() -> Iterator[PluginBase]:
    plugin = MockPlugin({}, return_value=("(value)",), return_expires_at=True)
    with patch("wev.resolver.get_plugin", return_value=plugin) as patched:
        yield patched


@fixture
def get_non_caching_plugin() -> Iterator[PluginBase]:
    plugin = MockPlugin({}, return_value=("(value)",), return_expires_at=False)
    with patch("wev.resolver.get_plugin", return_value=plugin) as patched:
        yield patched


@fixture
def get_plugin_cannot_resolve_error() -> Iterator[PluginBase]:
    plugin = MockPlugin({}, raises_cannot_resolve_error=True)
    with patch("wev.resolver.get_plugin", return_value=plugin) as patched:
        yield patched


@mark.parametrize(
    "resolution, expect",
    [
        (None, False),
        (Resolution.make(value=""), False),
        (
            Resolution.make(
                value=None, expires_at=datetime.now() - timedelta(seconds=60)
            ),
            False,
        ),
        (
            Resolution.make(
                value=None, expires_at=datetime.now() + timedelta(seconds=60)
            ),
            True,
        ),
    ],
)
def test_fresh_resolution(resolution: Optional[Resolution], expect: bool) -> None:
    expect_resolution = resolution if expect else None
    assert fresh_resolution(resolution=resolution) == expect_resolution


def test_resolve(get_plugin: Mock) -> None:
    environs = resolve(state=MockState())
    assert environs["alpha"] == "(value)"
    assert environs["beta"] == "(value)"
    assert environs["gamma"] == "gamma-value-old"
    assert environs["delta"] == "(value)"


def test_resolve__removes_cache(get_non_caching_plugin: Mock) -> None:
    state = MockState()
    state.resolution_cache.update(names=("alpha",), resolution=Mock())
    assert ("alpha",) in state.resolution_cache.resolutions
    resolve(state=state)
    assert ("alpha",) not in state.resolution_cache.resolutions


def test_resolve__cannot_resolve_error(get_plugin_cannot_resolve_error: Mock) -> None:
    with raises(CannotResolveError) as ex:
        resolve(state=MockState())
    assert str(ex.value) == '"alpha-handler" failed: cannot reticulate splines'
