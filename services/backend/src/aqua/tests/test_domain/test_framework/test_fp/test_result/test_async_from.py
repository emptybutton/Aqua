from pytest import mark
from result import Err, Ok

from aqua.domain.framework.fp.result import async_from


@mark.asyncio
async def test_with_ok() -> None:
    @async_from(Ok(2))
    @async_from(Ok(1))
    async def act(a: int, b: int, c: int) -> Ok[tuple[int, int, int]]:  # noqa: RUF029
        return Ok((a, b, c))

    assert await act(3) == Ok((1, 2, 3))


@mark.asyncio
async def test_with_err() -> None:
    @async_from(Err(4))
    @async_from(Ok(3))
    @async_from(Err(2))
    @async_from(Ok(1))
    async def act(a: int, b: int, c: int, d: int, e: int) -> Ok[  # noqa: RUF029
        tuple[int, int, int, int, int]
    ]:
        return Ok((a, b, c, d, e))

    assert await act(3) == Err(4)
