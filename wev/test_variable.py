from wev.variable import Variable


def test_plugin() -> None:
    assert (
        Variable(("foo",), store={"plugin": {"id": "wev-foo"}}).plugin.id == "wev-foo"
    )


def test_name() -> None:
    assert Variable(("foo",), store={}).names == ("foo",)
