import importlib.resources as pkg_resources


def get_version() -> str:
    """
    Gets the package version.

    Returns:
        str: Version.
    """
    with pkg_resources.open_text(__package__, "VERSION") as stream:
        return stream.readline().strip()
