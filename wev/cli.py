from argparse import ArgumentParser, RawDescriptionHelpFormatter
from typing import List, Optional

from colorama import Style

from wev.executor import execute
from wev.explainer import explain
from wev.logging import get_logger, set_level
from wev.sdk.exceptions import CannotResolveError
from wev.version import get_version


class CLI:
    """
    CLI executor.

    Arguments:
        args: Arguments. Will read from the command line if omitted.
    """

    def __init__(self, args: Optional[List[str]] = None) -> None:
        self.logger = get_logger()

        wev = Style.BRIGHT + "wev" + Style.RESET_ALL

        with_env_vars = (
            Style.BRIGHT
            + "w"
            + Style.RESET_ALL
            + "ith "
            + Style.BRIGHT
            + "e"
            + Style.RESET_ALL
            + "nvironment "
            + Style.BRIGHT
            + "v"
            + Style.RESET_ALL
            + "ariables"
        )

        description = f"{wev} runs shell commands {with_env_vars}."

        epilog = (
            "examples:\n"
            + "  wev --explain\n"
            + "  wev --version\n"
            + "  wev pipenv install\n"
            + "  wev --log-level DEBUG pipenv install\n"
            + "\n"
            + "Built with ❤️ by Cariad Eccleston: https://github.com/cariad/wev"
        )

        self.arg_parser = ArgumentParser(
            "wev",
            description=description,
            epilog=epilog,
            formatter_class=RawDescriptionHelpFormatter,
        )

        self.arg_parser.add_argument(
            "command",
            nargs="...",
            help=f"shell command and arguments to run {with_env_vars}.",
        )

        self.arg_parser.add_argument(
            "--explain",
            action="store_true",
            help=f"explain what {wev} will do",
        )

        self.arg_parser.add_argument(
            "--log-level",
            default="INFO",
            help="log level (default is INFO)",
            metavar="LEVEL",
        )

        self.arg_parser.add_argument(
            "--version",
            action="store_true",
            help="print the version",
        )

        self.args = self.arg_parser.parse_args(args)
        set_level(self.args.log_level.upper())

    def invoke(self) -> int:
        """
        Invokes the appropriate task for the given command line arguments

        Returns:
            Shell return code.
        """
        try:
            return self.try_invoke()
        except CannotResolveError as ex:
            self.logger.critical(ex)
            return 1
        except Exception as ex:
            self.logger.exception(ex)
            return 2

    def try_invoke(self) -> int:
        """
        Attempts to invokes the appropriate task for the given command line
        arguments. Could raise any exceptions.

        Returns:
            Shell return code.
        """
        if self.args.command:
            return execute(command=self.args.command)
        elif self.args.explain:
            explain()
        elif self.args.version:
            print(get_version())
        else:
            self.arg_parser.print_help()
        return 0
