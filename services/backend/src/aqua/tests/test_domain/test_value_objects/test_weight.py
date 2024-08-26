from pytest import raises

from aqua.domain import value_objects as vos


def test_invalid_amount() -> None:
    with raises(vos.Weight.IncorrectAmountError):
        vos.Weight(kilograms=-1)
