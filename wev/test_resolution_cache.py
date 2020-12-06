from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator, Optional

from pytest import fixture, raises

from wev import ResolutionCache
from wev.exceptions import CacheReadError
from wev.log import init
from wev.sdk import Resolution


@fixture
def cache_path() -> Iterator[Path]:
    init("DEBUG")
    with TemporaryDirectory() as cache_dir:
        yield Path(cache_dir).joinpath(".wevcache")


def make_cache(path: Optional[Path] = None) -> ResolutionCache:
    return ResolutionCache(context="", path=path)


def test_read__corrupt(cache_path: Path) -> None:
    with open(cache_path, "w") as stream:
        stream.write("{")

    with raises(CacheReadError) as ex:
        make_cache(path=cache_path).load()

    assert str(ex.value) == (
        f'Could not read cache at "{cache_path}": '
        "Expecting property name enclosed in double quotes: "
        "line 1 column 2 (char 1)"
    )


def test_read__empty(cache_path: Path) -> None:
    with open(cache_path, "w") as stream:
        stream.write("")

    cache = make_cache(path=cache_path)
    cache.load()
    assert cache.resolutions == {}


def test_read__not_exists(cache_path: Path) -> None:
    cache = make_cache(path=cache_path)
    cache.load()
    assert cache.resolutions == {}


def test_write_then_read(cache_path: Path) -> None:
    resolution = Resolution.make(value="bar")
    writer = make_cache(path=cache_path)
    writer.update(var_name="foo", resolution=resolution)
    writer.save()

    reader = make_cache(path=cache_path)
    reader.load()
    assert len(reader.resolutions) == 1
    assert reader.get("foo") == resolution


def test_update__add_then_get() -> None:
    resolution_a = Resolution.make(value="")
    resolution_b = Resolution.make(value="")
    cache = make_cache()
    cache.update(var_name="alpha", resolution=resolution_a)
    cache.update(var_name="beta", resolution=resolution_b)
    assert len(cache.resolutions) == 2
    assert cache.get("alpha") is resolution_a
    assert cache.get("beta") is resolution_b


def test_update__update_then_get() -> None:
    resolution_a = Resolution.make(value="")
    resolution_b = Resolution.make(value="")
    cache = make_cache()
    cache.update(var_name="alpha", resolution=resolution_a)
    cache.update(var_name="alpha", resolution=resolution_b)
    assert len(cache.resolutions) == 1
    assert cache.get("alpha") is resolution_b


def test_update_then_remove() -> None:
    resolution_a = Resolution.make(value="")
    resolution_b = Resolution.make(value="")
    cache = make_cache()
    cache.update(var_name="alpha", resolution=resolution_a)
    cache.update(var_name="beta", resolution=resolution_b)
    cache.remove("alpha")
    assert len(cache.resolutions) == 1
    assert cache.get("alpha") is None
    assert cache.get("beta") is resolution_b


def test_remove__not_exists() -> None:
    # Just assert that it doesn't raise an exception.
    make_cache().remove("alpha")
