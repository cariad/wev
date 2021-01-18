from mock import Mock, patch

from wev.text.datetime import get_now


@patch("wev.text.datetime.datetime")
def test_get_now(datetime: Mock) -> None:
    strftime = Mock(return_value="foo")
    now = Mock()
    now.strftime = strftime
    now_maker = Mock(return_value=now)
    datetime.now = now_maker
    assert get_now() == "foo"
    now_maker.assert_called_once_with()
    strftime.assert_called_once_with("%Y-%m-%d %H:%M:%S")
