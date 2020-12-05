from datetime import datetime

from colorama import Style

from wev import Cache, get_plugin, get_variables, get_version


def explain() -> None:
    cache = Cache()
    cache.read()
    print()
    print(
        Style.BRIGHT,
        "wev",
        Style.RESET_ALL,
        f" ({get_version()}) execution plan generated at ",
        Style.BRIGHT,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        Style.RESET_ALL,
        ":",
        sep="",
    )
    print()
    for index, variable in enumerate(get_variables(cache=cache)):
        num = str(index + 1).rjust(2) + "."
        name = Style.BRIGHT + variable.name + Style.RESET_ALL
        handler = Style.BRIGHT + variable.handler + Style.RESET_ALL

        print(f"{num} {name} will be resolved by the {handler} plugin.")

        margin = "  "

        if variable.resolution:
            print()
            seconds = variable.resolution.seconds_until_expiry
            if seconds is not None and seconds > 0:
                print(
                    margin,
                    Style.DIM,
                    f"The cached value will be used for another {seconds} seconds.",
                    Style.RESET_ALL,
                )
            elif seconds is not None and seconds <= 0:
                print(
                    margin,
                    Style.DIM,
                    f"The cached value expired {0-seconds} seconds ago. ",
                    "The cache will be refreshed.",
                    Style.RESET_ALL,
                )

        print()
        plugin = get_plugin(variable)
        for line in plugin.explain():
            print(f"    {Style.DIM}{line}{Style.RESET_ALL}")
        print()
