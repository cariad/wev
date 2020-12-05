from pytest import mark

from wev.sdk.exceptions import MissingConfigurationError


@mark.parametrize(
    "ex, expect",
    [
        (
            MissingConfigurationError(key="foo"),
            'The "foo" configuration key is required.',
        ),
        (
            MissingConfigurationError(key="foo", explanation="bar"),
            'The "foo" configuration key is required: bar',
        ),
    ],
)
def test_missing_configuration_error(
    ex: MissingConfigurationError,
    expect: str,
) -> None:
    assert str(ex) == expect
