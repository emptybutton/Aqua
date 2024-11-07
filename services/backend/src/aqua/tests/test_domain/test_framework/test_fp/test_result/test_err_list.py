from aqua.domain.framework.fp.result import ErrList, OkList


def test_map() -> None:
    result = ErrList(4).map("X")

    assert result == ErrList(4)


def test_map_err() -> None:
    result = ErrList(4).map_err(lambda v: -v)

    assert result == ErrList(-4)


def test_add_with_ok_list() -> None:
    result = OkList((1, )) + OkList((2, )) + OkList((3, ))

    assert result == OkList((1, 2, 3))


def test_add_with_err_list() -> None:
    result = OkList((1, )) + ErrList(2) + ErrList(3)

    assert result == ErrList(2)
