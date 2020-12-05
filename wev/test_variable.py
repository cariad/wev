from wev.variable import Variable


def test_handler() -> None:
    assert Variable(name="foo", values={"handler": "wev-foo"}).handler == "wev-foo"


def test_name() -> None:
    assert Variable(name="foo", values={}).name == "foo"
