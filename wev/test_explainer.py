from datetime import datetime
from logging import Logger
from typing import Iterator, List

from mock import Mock, call, patch
from pytest import fixture

from wev.explainer import explain
from wev.sdk import PluginBase, Resolution
from wev.variable import Variable


class MockPlugin(PluginBase):
    def explain(self) -> List[str]:
        return ["(explanation)"]

    def resolve(self, logger: Logger) -> Resolution:
        pass


@fixture
def get_variables() -> Iterator[Iterator[Variable]]:
    mock_now = "2020-01-01T00:00:01"

    var_a = Variable(name="alpha", values={"handler": "alpha-handler"})

    var_b = Variable(
        name="beta",
        values={"handler": "beta-handler", "resolution": {"value": ""}},
    )

    var_c = Variable(
        name="gamma",
        values={
            "handler": "gamma-handler",
            "resolution": {"expires_at": "2020-01-01T00:00:02"},
        },
    )

    var_d = Variable(
        name="delta",
        values={
            "handler": "delta-handler",
            "resolution": {"expires_at": "2020-01-01T00:00:00"},
        },
    )

    v = [var_a, var_b, var_c, var_d]
    with patch("wev.sdk.resolution.datetime") as patched_datetime:
        patched_datetime.now = Mock(return_value=datetime.fromisoformat(mock_now))
        patched_datetime.fromisoformat = datetime.fromisoformat
        with patch("wev.explainer.get_variables", return_value=iter(v)) as patched:
            yield patched


@fixture
def get_plugin() -> Iterator[PluginBase]:
    with patch("wev.explainer.get_plugin", return_value=MockPlugin()) as get_plugin:
        yield get_plugin


@patch("wev.explainer.get_now", return_value="(now)")
def test(
    get_now: Mock,
    get_plugin: PluginBase,
    get_variables: Iterator[Variable],
) -> None:
    logger = Mock()
    explain(logger=logger)

    expect_info = [
        call(
            "%s (%s) execution plan generated at %s:",
            "\x1b[1mwev\x1b[22m",
            "-1.-1.-1",
            "\x1b[1m(now)\x1b[22m",
        ),
        call(""),
        call(
            "%s%s %s will be resolved by the %s plugin.",
            " 1",
            ".",
            "\x1b[1malpha\x1b[22m",
            "\x1b[1malpha-handler\x1b[22m",
        ),
        call(""),
        call("%s%s", "    ", "\x1b[2m(explanation)\x1b[22m"),
        call(""),
        call(
            "%s%s %s will be resolved by the %s plugin.",
            " 2",
            ".",
            "\x1b[1mbeta\x1b[22m",
            "\x1b[1mbeta-handler\x1b[22m",
        ),
        call(""),
        call(
            "%s%s",
            "    ",
            "\x1b[2mThe value is never cached.\x1b[22m",
        ),
        call(""),
        call("%s%s", "    ", "\x1b[2m(explanation)\x1b[22m"),
        call(""),
        call(
            "%s%s %s will be resolved by the %s plugin.",
            " 3",
            ".",
            "\x1b[1mgamma\x1b[22m",
            "\x1b[1mgamma-handler\x1b[22m",
        ),
        call(""),
        call(
            "%s%s",
            "    ",
            "\x1b[2mThe cached value will expire in 1 seconds.\x1b[22m",
        ),
        call(""),
        call(
            "%s%s %s will be resolved by the %s plugin.",
            " 4",
            ".",
            "\x1b[1mdelta\x1b[22m",
            "\x1b[1mdelta-handler\x1b[22m",
        ),
        call(""),
        call(
            "%s%s",
            "    ",
            "\x1b[2mThe cached value expired 1 seconds ago.\x1b[22m",
        ),
        call(""),
        call("%s%s", "    ", "\x1b[2m(explanation)\x1b[22m"),
    ]

    assert logger.info.call_count == len(expect_info)
    logger.info.assert_has_calls(expect_info)
