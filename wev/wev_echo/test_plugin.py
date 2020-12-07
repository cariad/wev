from logging import Logger

from pytest import raises

from wev.sdk import ResolutionSupport
from wev.sdk.exceptions import MissingConfigurationError
from wev.wev_echo import Plugin


def test_explain(logger: Logger) -> None:
    assert Plugin().explain(logger=logger) == [
        "The environment variable will be set directly to the configured value."
    ]


def test_resolve(resolution_support: ResolutionSupport) -> None:
    resolution = Plugin({"value": "foo"}).resolve(support=resolution_support)
    assert resolution.values == ("foo",)


def test_resolve__missing_config(resolution_support: ResolutionSupport) -> None:
    with raises(MissingConfigurationError) as ex:
        Plugin({"foo": "bar"}).resolve(support=resolution_support)
    assert str(ex.value) == (
        "The 'value' key is required in {'foo': 'bar'}: "
        "This is the value that will be echoed."
    )
