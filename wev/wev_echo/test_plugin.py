from logging import getLogger

from pytest import raises

from wev.sdk.exceptions import MissingConfigurationError
from wev.wev_echo import Plugin


def test_explain() -> None:
    assert Plugin().explain() == [
        "The environment variable will be set directly to the configured value."
    ]


def test_resolve() -> None:
    assert Plugin({"value": "foo"}).resolve(logger=getLogger("wev")).value == "foo"


def test_resolve__missing_config() -> None:
    with raises(MissingConfigurationError) as ex:
        Plugin({}).resolve(logger=getLogger("wev"))
    assert str(ex.value) == (
        'The "value" configuration key is required: '
        "This is the value that will be echoed."
    )
