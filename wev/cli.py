from argparse import ArgumentParser
from logging import getLogger
from typing import List, Optional

from wev.executor import execute
from wev.explainer import explain
from wev.log import init, set_level
from wev.version import get_version


class CLI:
    """
    CLI executor.

    Arguments:
        args (List[str]): Optional arguments. Will read from the command line if
                          omitted. Intended for tests.
    """

    def __init__(self, args: Optional[List[str]] = None) -> None:
        init()
        self.logger = getLogger()

        self.arg_parser = ArgumentParser(
            "wev",
            description="`wev` runs shell commands With Environment Variables..",
            epilog="Homepage: https://github.com/cariad/wev",
        )

        self.arg_parser.add_argument(
            "--version",
            action="store_true",
            help="print the version",
        )
        self.arg_parser.add_argument(
            "--explain",
            action="store_true",
            help="explain what `wev` will do",
        )
        self.arg_parser.add_argument("command", nargs="...")
        self.arg_parser.add_argument("--log-level", default="INFO")
        self.args = self.arg_parser.parse_args(args)
        set_level(self.args.log_level)

    def try_invoke(self) -> int:
        if self.args.command:
            return execute(command=self.args.command)
        elif self.args.explain:
            explain()
        elif self.args.version:
            self.logger.info(get_version())
        else:
            self.arg_parser.print_help()
        return 0

    def invoke(self) -> int:
        """
        Invokes the apppriate task for the given command line arguments.

        Returns:
            int: Shell return code.
        """
        try:
            return self.try_invoke()
        except Exception as ex:
            self.logger.critical(ex)
            return 1
