from result import Err

from aqua.domain.model.primitives.vos.water import (
    NegativeWaterAmountError,
    Water,
)


def test_valid_amount() -> None:
    Water.with_(milliliters=0).unwrap()


def test_invalid_amount() -> None:
    result = Water.with_(milliliters=-1)

    assert result == Err(NegativeWaterAmountError())


def test_sum() -> None:
    water1 = Water.with_(milliliters=250).unwrap()
    water2 = Water.with_(milliliters=500).unwrap()
    expected_sum = Water.with_(milliliters=750).unwrap()

    sum_ = water1 + water2

    assert sum_ == expected_sum
