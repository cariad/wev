# from datetime import datetime
from logging import Logger
from typing import Iterator, List

from mock import Mock, call, patch
from pytest import fixture

from wev.explainer import explain
from wev.sdk import PluginBase, Resolution
from wev.state import MockState


class MockPlugin(PluginBase):
    def explain(self) -> List[str]:
        return ["(explanation)"]

    def resolve(self, logger: Logger) -> Resolution:
        pass


@fixture
def get_plugin() -> Iterator[PluginBase]:
    plugin = MockPlugin(config={})
    with patch("wev.explainer.get_plugin", return_value=plugin) as patched:
        yield patched


@patch("wev.explainer.get_now", return_value="(now)")
def test(get_now: Mock, get_plugin: PluginBase) -> None:
    logger = Mock()
    explain(logger=logger, state=MockState())

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
            "\x1b[2mThe cached value will expire in 59 seconds.\x1b[22m",
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
            "\x1b[2mThe cached value expired 60 seconds ago.\x1b[22m",
        ),
        call(""),
        call("%s%s", "    ", "\x1b[2m(explanation)\x1b[22m"),
        call(""),
    ]

    assert logger.info.call_count == len(expect_info)
    logger.info.assert_has_calls(expect_info)
