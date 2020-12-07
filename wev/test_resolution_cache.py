from logging import Logger
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator, Optional

from pytest import fixture, raises

from wev import ResolutionCache
from wev.exceptions import CacheReadError
from wev.sdk import Resolution


@fixture
def cache_path() -> Iterator[Path]:
    with TemporaryDirectory() as cache_dir:
        yield Path(cache_dir).joinpath(".wevcache")


def make_cache(
    logger: Optional[Logger] = None, path: Optional[Path] = None
) -> ResolutionCache:
    return ResolutionCache(context="test", logger=logger, path=path)


def test_read__corrupt(cache_path: Path) -> None:
    with open(cache_path, "w") as stream:
        stream.write("{")

    with raises(CacheReadError) as ex:
        make_cache(path=cache_path).load()

    assert str(ex.value) == (
        f'Could not read cache at "{cache_path}": while parsing a flow node\n'
        "expected the node content, but found '<stream end>'\n"
        '  in "<unicode string>", line 1, column 2:\n'
        "    {\n"
        "     ^ (line: 1)"
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


def test_write_then_read(cache_path: Path, logger: Logger) -> None:
    resolution = Resolution.make(value="bar")
    writer = make_cache(logger=logger, path=cache_path)
    writer.update(("foo",), resolution=resolution)
    writer.save()

    reader = make_cache(path=cache_path)
    reader.load()
    assert len(reader.resolutions) == 1
    assert reader.get(("foo",)) == resolution


def test_update__add_then_get() -> None:
    resolution_a = Resolution.make(value="")
    resolution_b = Resolution.make(value="")
    cache = make_cache()
    cache.update(("alpha",), resolution=resolution_a)
    cache.update(("beta",), resolution=resolution_b)
    assert len(cache.resolutions) == 2
    assert cache.get(("alpha",)) == resolution_a
    assert cache.get(("beta",)) == resolution_b


def test_update__update_then_get() -> None:
    resolution_a = Resolution.make(value="")
    resolution_b = Resolution.make(value="")
    cache = make_cache()
    cache.update(("alpha",), resolution=resolution_a)
    cache.update(("alpha",), resolution=resolution_b)
    assert len(cache.resolutions) == 1
    assert cache.get(("alpha",)) == resolution_b


def test_update_then_remove() -> None:
    resolution_a = Resolution.make(value="")
    resolution_b = Resolution.make(value="")
    cache = make_cache()
    cache.update(("alpha",), resolution=resolution_a)
    cache.update(("beta",), resolution=resolution_b)
    cache.remove(("alpha",))
    assert len(cache.resolutions) == 1
    assert cache.get(("alpha",)) is None
    assert cache.get(("beta",)) == resolution_b


def test_remove__not_exists() -> None:
    # Just assert that it doesn't raise an exception.
    make_cache().remove(("alpha",))
