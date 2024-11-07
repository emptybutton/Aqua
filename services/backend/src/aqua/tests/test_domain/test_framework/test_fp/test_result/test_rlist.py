from result import Err, Ok

from aqua.domain.framework.fp.result import ErrList, OkList, rlist


def test_with_ok() -> None:
    result = rlist(Ok(1))

    assert result == OkList((1, ))


def test_with_err() -> None:
    result = rlist(Err(2))

    assert result == ErrList(2)
