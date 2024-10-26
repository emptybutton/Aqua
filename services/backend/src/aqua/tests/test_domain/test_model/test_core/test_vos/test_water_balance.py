from result import Err, Ok

from aqua.domain.model.core.vos.water_balance import (
    ExtremeWeightForSuitableWaterBalanceError,
    WaterBalance,
)
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight


def test_middle_suitable() -> None:
    weight = Weight.with_(kilograms=70).unwrap()
    water = Water.with_(milliliters=2000).unwrap()
    expected_result = Ok(WaterBalance(water=water))

    result = WaterBalance.suitable_when(weight=weight)

    assert result == expected_result


def test_low_suitable() -> None:
    weight = Weight.with_(kilograms=30).unwrap()
    water = Water.with_(milliliters=1600).unwrap()
    expected_result = Ok(WaterBalance(water=water))

    result = WaterBalance.suitable_when(weight=weight)

    assert result == expected_result


def test_high_suitable() -> None:
    weight = Weight.with_(kilograms=150).unwrap()
    water = Water.with_(milliliters=2800).unwrap()
    expected_result = Ok(WaterBalance(water=water))

    result = WaterBalance.suitable_when(weight=weight)

    assert result == expected_result


def test_invalid_high_suitable() -> None:
    weight = Weight.with_(kilograms=151).unwrap()
    expected_result = Err(ExtremeWeightForSuitableWaterBalanceError())

    result = WaterBalance.suitable_when(weight=weight)

    assert expected_result == result


def test_invalid_low_suitable() -> None:
    weight = Weight.with_(kilograms=29).unwrap()
    expected_result = Err(ExtremeWeightForSuitableWaterBalanceError())

    result = WaterBalance.suitable_when(weight=weight)

    assert expected_result == result
