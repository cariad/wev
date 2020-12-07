from datetime import datetime, timedelta
from typing import Iterator, Optional

from mock import Mock, patch
from pytest import fixture, mark

from wev.mock_plugin import MockPlugin
from wev.resolver import fresh_resolution, resolve
from wev.sdk import PluginBase, Resolution
from wev.state import MockState


@fixture
def get_plugin() -> Iterator[PluginBase]:
    plugin = MockPlugin(config={})
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
