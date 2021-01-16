from mock import Mock, patch
from pytest import raises

from wev.exceptions import MultiplePluginsError, NoPluginError
from wev.plugins import get_plugin
from wev.sdk import PluginConfiguration


def test_get_plugin() -> None:
    plugin = get_plugin(PluginConfiguration({"id": "wev-echo"}))
    assert plugin.version == "1.0.0"


def test_get_plugin__no_match() -> None:
    with raises(NoPluginError) as ex:
        get_plugin(PluginConfiguration({"id": "none"}))
    assert str(ex.value) == '"none" isn\'t installed. Try "pip3 install none"?'


def mock_entry_point(name: str) -> Mock:
    entry_point = Mock()
    entry_point.name = name
    return entry_point


@patch("wev.plugins.iter_entry_points")
def test_get_plugin__multiple_matches(iter_entry_points: Mock) -> None:
    iter_entry_points.return_value = [
        mock_entry_point(name="several"),
        mock_entry_point(name="several"),
    ]

    with raises(MultiplePluginsError) as ex:
        get_plugin(PluginConfiguration({"id": "several"}))
    assert str(ex.value) == '2 plugins are claiming to be "several".'
