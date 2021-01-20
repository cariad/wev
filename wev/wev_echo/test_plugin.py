from logging import Logger
from typing import Any, Dict

from pytest import mark, raises

from wev.sdk import ResolutionSupport
from wev.sdk.exceptions import MissingConfigurationError
from wev.wev_echo import Plugin


def test_explain(logger: Logger) -> None:
    assert Plugin().explain(logger=logger) == [
        "The environment variable will be set directly to the configured value."
    ]


@mark.parametrize(
    "d, expect",
    [
        ({"value": "foo"}, ("foo",)),
        ({"value": ["foo", "bar"]}, ("foo bar",)),
        ({"separator": ".", "value": ["foo", "bar"]}, ("foo.bar",)),
    ],
)
def test_resolve(
    d: Dict[str, Any],
    expect: str,
    resolution_support: ResolutionSupport,
) -> None:
    assert Plugin(d).resolve(support=resolution_support).values == expect


def test_resolve__missing_config(resolution_support: ResolutionSupport) -> None:
    with raises(MissingConfigurationError) as ex:
        Plugin({"foo": "bar"}).resolve(support=resolution_support)
    assert str(ex.value) == (
        "The 'value' key is required in this plugin's configuration: "
        "This is the value that will be echoed."
    )


def test_version() -> None:
    assert Plugin({}).version == "1.0.0"


def test_str() -> None:
    assert str(Plugin({})) == "version 1.0.0"
