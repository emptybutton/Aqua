from pytest import raises

from aqua.domain import value_objects as vos


def test_invalid_amount() -> None:
    with raises(vos.Water.IncorrectAmountError):
        vos.Water(milliliters=-1)


def test_sum() -> None:
    water1 = vos.Water(milliliters=250)
    water2 = vos.Water(milliliters=500)
    expected_sum = vos.Water(milliliters=750)
    sum_ = water1 + water2

    assert sum_ == expected_sum

