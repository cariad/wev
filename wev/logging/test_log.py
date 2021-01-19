from mock import Mock, patch

from wev.logging.formatter import Formatter
from wev.logging.log import get_logger


@patch("wev.logging.log.StreamHandler")
@patch("wev.logging.log.getLogger")
@patch("wev.logging.log.stdout")
def test_get_logger__adds_handler(
    stdout: Mock,
    logger_maker: Mock,
    stream_handler_maker: Mock,
) -> None:
    stream_handler = Mock()
    stream_handler_maker.return_value = stream_handler

    logger = Mock()
    logger_maker.return_value = logger

    addHandler = Mock()
    logger.addHandler = addHandler

    not_our_handler = Mock()
    not_our_handler.formatter = Mock()
    logger.handlers = [not_our_handler]

    assert get_logger()

    stream_handler_maker.assert_called_once_with(stdout)
    addHandler.assert_called_once_with(stream_handler)


@patch("wev.logging.log.getLogger")
def test_get_logger__adds_handler_once(logger_maker: Mock) -> None:
    stream_handler = Mock()
    stream_handler.formatter = Formatter(name="test")

    logger = Mock()
    logger_maker.return_value = logger

    addHandler = Mock()
    logger.addHandler = addHandler

    logger.handlers = [stream_handler]

    get_logger()

    addHandler.assert_not_called()
