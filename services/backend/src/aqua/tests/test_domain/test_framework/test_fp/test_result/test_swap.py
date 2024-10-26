from result import Err, Ok, Result

from aqua.domain.framework.fp.result import swap


def test_with_ok() -> None:
    value: Result[int, str] = Ok(42)
    result = swap(value)

    assert result == Err(42)


def test_with_err() -> None:
    value: Result[str, int] = Err(42)
    result = swap(value)

    assert result == Ok(42)
