# from mock import Mock, patch

# from wev.cli import CLI


# def test_args() -> None:
#     assert not CLI().args.command
#     assert not CLI().args.info
#     assert not CLI().args.profile
#     assert not CLI().args.version


# def test_args__command() -> None:
#     assert CLI(["pipenv", "sync"]).args.command == ["pipenv", "sync"]


# def test_args__info() -> None:
#     assert CLI(["--info"]).args.info


# def test_args__profile() -> None:
#     assert CLI(["--profile", "foo"]).args.profile == "foo"


# def test_args__version() -> None:
#     assert CLI(["--version"]).args.version


# @patch("corf.cli.Executor")
# def test_execute__success(executor_maker: Mock) -> None:
#     executor = Mock()
#     executor.execute.return_value = 0
#     executor_maker.return_value = executor
#     assert CLI().execute() == 0
#     assert executor_maker.called_with()
#     assert executor.execute.called_with()


# @patch("corf.cli.Executor")
# def test_execute__fail(executor_maker: Mock) -> None:
#     executor = Mock()
#     executor.execute.side_effect = Exception("printer on fire")
#     executor_maker.return_value = executor
#     assert CLI().execute() == 1


# @patch("corf.cli.CLI.print_help", return_value=0)
# @patch("corf.cli.CLI.setup_logging")
# def test_invoke(setup_logging: Mock, print_help: Mock) -> None:
#     assert CLI([]).invoke() == 0
#     setup_logging.assert_called_with()
#     print_help.assert_called_with()


# @patch("corf.cli.CLI.execute", return_value=0)
# def test_invoke__command(execute: Mock) -> None:
#     assert CLI(["pipenv", "sync"]).invoke() == 0
#     execute.assert_called_with()


# @patch("corf.cli.CLI.print_info", return_value=0)
# def test_invoke__info(print_info: Mock) -> None:
#     assert CLI(["--info"]).invoke() == 0
#     print_info.assert_called_with()


# @patch("corf.cli.CLI.print_version", return_value=0)
# def test_invoke__version(print_version: Mock) -> None:
#     assert CLI(["--version"]).invoke() == 0
#     print_version.assert_called_with()


# def test_make_arg_parser() -> None:
#     assert CLI().make_arg_parser()


# def test_print_help() -> None:
#     assert CLI().print_help() == 0


# def test_print_info() -> None:
#     assert CLI().print_info() == 0


# def test_print_version() -> None:
#     assert CLI().print_version() == 0


# @patch("corf.cli.getLogger")
# def test_setup_logging__boto(get_logger: Mock) -> None:
#     CLI().setup_logging()
#     get_logger.assert_called_with("boto")
#     get_logger.return_value.setLevel.assert_called_with("CRITICAL")


# def test_setup_logging__succeeds() -> None:
#     CLI().setup_logging()
#     assert True
