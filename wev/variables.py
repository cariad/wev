from typing import Iterator

from dwalk import dwalk

from wev import Variable
from wev.cache import Cache


def get_variables(cache: Cache) -> Iterator[Variable]:
    config = dwalk(filenames=[".wev.yml", ".wev.user.yml"])

    for var_name in config:
        values = {**config[var_name], "resolution": cache.get(var_name=var_name)}

        yield Variable(name=var_name, values=values)
