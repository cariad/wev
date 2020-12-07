from pytest import mark

from wev.sdk.exceptions import MissingConfigurationError


@mark.parametrize(
    "ex, expect",
    [
        (
            MissingConfigurationError(config={"fooo": "bar"}, key="foo"),
            "The foo key is required in {'fooo': 'bar'}.",
        ),
        (
            MissingConfigurationError(
                config={"fooo": "bar"},
                key="foo",
                explanation="bar",
            ),
            "The foo key is required in {'fooo': 'bar'}: bar",
        ),
    ],
)
def test_missing_configuration_error(
    ex: MissingConfigurationError,
    expect: str,
) -> None:
    assert str(ex) == expect
