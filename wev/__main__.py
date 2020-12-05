from wev.cli import CLI


def cli_entry() -> None:
    exit(CLI().invoke())


if __name__ == "__main__":
    cli_entry()
