from mock import Mock, patch

from wev.cli import CLI
from wev.sdk.exceptions import CannotResolveError


def test_args() -> None:
    assert not CLI().args.command
    assert not CLI().args.explain
    assert not CLI().args.version
    assert CLI().args.log_level == "INFO"


@patch("wev.cli.execute", return_value=0)
def test_command(execute: Mock) -> None:
    cli = CLI(["pipenv", "sync"])
    assert cli.args.command == ["pipenv", "sync"]
    assert cli.invoke() == 0
    execute.assert_called_with(command=["pipenv", "sync"])


@patch("wev.cli.execute", side_effect=CannotResolveError())
def test_command__cannot_resolve_error(execute: Mock) -> None:
    assert CLI(["pipenv", "sync"]).invoke() == 1


@patch("wev.cli.execute", side_effect=Exception())
def test_command__unhandled_error(execute: Mock) -> None:
    assert CLI(["pipenv", "sync"]).invoke() == 2


@patch("wev.cli.explain")
def test_args__explain(explain: Mock) -> None:
    cli = CLI(["--explain"])
    assert cli.args.explain
    assert cli.invoke() == 0
    explain.assert_called_with()


@patch("wev.cli.get_version")
def test_args__version(get_version: Mock) -> None:
    cli = CLI(["--version"])
    assert cli.args.version
    assert cli.invoke() == 0
    get_version.assert_called_with()


@patch("wev.cli.ArgumentParser.print_help")
def test_args__help(print_help: Mock) -> None:
    cli = CLI([])
    assert cli.invoke() == 0
    print_help.assert_called_with()
