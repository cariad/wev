from datetime import datetime, timedelta
from logging import Logger, basicConfig, root
from typing import Iterator, List, Optional

from mock import Mock, patch
from pytest import fixture, mark

from wev import Variable
from wev.resolver import fresh_resolution, resolve
from wev.sdk import PluginBase, Resolution

future = datetime.now() + timedelta(seconds=60)
past = datetime.now() - timedelta(seconds=60)


class MockPlugin(PluginBase):
    def explain(self) -> List[str]:
        return ["(explanation)"]

    def resolve(self, logger: Logger) -> Resolution:
        logger.debug("Setting value...")
        return Resolution.make(value="(value)", expires_at=future)


@fixture
def get_plugin() -> Iterator[PluginBase]:
    plugin = MockPlugin(config={})
    with patch("wev.resolver.get_plugin", return_value=plugin) as patched:
        yield patched


@fixture
def get_variables() -> Iterator[Iterator[Variable]]:
    var_a = Variable(name="alpha", values={"handler": "alpha-handler"})

    var_b = Variable(
        name="beta",
        values={"handler": "beta-handler", "resolution": {"value": "beta-value-old"}},
    )

    var_c = Variable(
        name="gamma",
        values={
            "handler": "gamma-handler",
            "resolution": {
                "expires_at": future.isoformat(),
                "value": "gamma-value-old",
            },
        },
    )

    var_d = Variable(
        name="delta",
        values={
            "handler": "delta-handler",
            "resolution": {"expires_at": past.isoformat(), "value": "delta-value-old"},
        },
    )

    v = [var_a, var_b, var_c, var_d]
    with patch("wev.resolver.get_variables", return_value=iter(v)) as patched:
        yield patched


@mark.parametrize(
    "resolution, expect",
    [
        (None, False),
        (Resolution.make(value=""), False),
        (Resolution.make(value="", expires_at=past), False),
        (Resolution.make(value="", expires_at=future), True),
    ],
)
def test_fresh_resolution(resolution: Optional[Resolution], expect: bool) -> None:
    expect_resolution = resolution if expect else None
    assert fresh_resolution(resolution=resolution) == expect_resolution


def test_resolve(get_variables: Mock, get_plugin: Mock) -> None:
    basicConfig()
    root.setLevel("DEBUG")
    environs = resolve()
    assert environs["alpha"] == "(value)"
    assert environs["beta"] == "(value)"
    assert environs["gamma"] == "gamma-value-old"
    assert environs["delta"] == "(value)"
