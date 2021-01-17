from typing import Iterator

from mock import Mock, call, patch
from pytest import fixture

from wev.explainer import explain
from wev.mock_plugin import MockPlugin
from wev.sdk import PluginBase
from wev.state import MockState


@fixture
def get_plugin() -> Iterator[PluginBase]:
    plugin = MockPlugin({})
    with patch("wev.explainer.get_plugin", return_value=plugin) as patched:
        yield patched


@patch("wev.explainer.get_now", return_value="(now)")
@patch("wev.explainer.get_version", return_value="(version)")
def test(get_version: Mock, get_now: Mock, get_plugin: PluginBase) -> None:
    logger = Mock()
    explain(logger=logger, state=MockState())

    expect_info = [
        call(
            "%s (%s) execution plan generated at %s:",
            "\x1b[1mwev\x1b[22m",
            "(version)",
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
