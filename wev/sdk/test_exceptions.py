from pytest import mark

from wev.sdk.exceptions import MissingConfigurationError


@mark.parametrize(
    "ex, expect",
    [
        (
            MissingConfigurationError(key="foo"),
            "The foo key is required in this plugin's configuration.",
        ),
        (
            MissingConfigurationError(
                key="foo",
                explanation="bar",
            ),
            "The foo key is required in this plugin's configuration: bar",
        ),
    ],
)
def test_missing_configuration_error(
    ex: MissingConfigurationError,
    expect: str,
) -> None:
    assert str(ex) == expect
