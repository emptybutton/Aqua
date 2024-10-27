from pytest import mark
from result import Err, Ok

from aqua.domain.framework.fp.result import sync


@mark.asyncio
async def test_with_ok() -> None:
    async def same[V](v: V) -> V:  # noqa: RUF029
        return v

    async_result = Ok(same(4))

    assert await sync(async_result) == Ok(4)


@mark.asyncio
async def test_with_err() -> None:
    assert await sync(Err(4)) == Err(4)
