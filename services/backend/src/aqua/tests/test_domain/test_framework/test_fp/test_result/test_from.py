from result import Err, Ok

from aqua.domain.framework.fp.result import from_


def test_with_ok() -> None:
    @from_(Ok(2))
    @from_(Ok(1))
    def act(a: int, b: int, c: int) -> Ok[tuple[int, int, int]]:
        return Ok((a, b, c))

    assert act(3) == Ok((1, 2, 3))


def test_with_err() -> None:
    @from_(Err(4))
    @from_(Ok(3))
    @from_(Err(2))
    @from_(Ok(1))
    def act(
        a: int, b: int, c: int, d: int, e: int
    ) -> Ok[tuple[int, int, int, int, int]]:
        return Ok((a, b, c, d, e))

    assert act(3) == Err(4)
