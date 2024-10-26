from result import Err

from aqua.domain.model.primitives.vos.weight import (
    NegativeWeightAmountError,
    Weight,
)


def test_valid_amount() -> None:
    Weight.with_(kilograms=0).unwrap()


def test_invalid_amount() -> None:
    result = Weight.with_(kilograms=-1)

    assert result == Err(NegativeWeightAmountError())
