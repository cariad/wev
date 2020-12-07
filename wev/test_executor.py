from typing import Iterator

from mock import Mock, patch
from pytest import fixture

from wev.executor import execute


@fixture
def run() -> Iterator[Mock]:
    with patch("wev.executor.run") as run:
        run.return_value.returncode = 0
        yield run


@patch("wev.executor.resolve", return_value={"foo": "bar"})
def test(resolve: Mock, run: Mock) -> None:
    assert execute(["pipenv", "install"]) == 0
    run.assert_called_with(["pipenv", "install"], env={"foo": "bar"})
