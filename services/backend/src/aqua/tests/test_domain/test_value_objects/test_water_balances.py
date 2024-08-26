from pytest import raises

from aqua.domain import value_objects as vos


def test_middle_suitable() -> None:
    weight = vos.Weight(kilograms=70)
    water = vos.Water(milliliters=2000)
    expected_suitable_balance = vos.WaterBalance(water=water)

    suitable_balance = vos.WaterBalance.suitable_when(weight=weight)

    assert suitable_balance == expected_suitable_balance


def test_low_suitable() -> None:
    weight = vos.Weight(kilograms=30)
    water = vos.Water(milliliters=1600)
    expected_suitable_balance = vos.WaterBalance(water=water)

    suitable_balance = vos.WaterBalance.suitable_when(weight=weight)

    assert suitable_balance == expected_suitable_balance


def test_high_suitable() -> None:
    weight = vos.Weight(kilograms=150)
    water = vos.Water(milliliters=2800)
    expected_suitable_balance = vos.WaterBalance(water=water)

    suitable_balance = vos.WaterBalance.suitable_when(weight=weight)

    assert suitable_balance == expected_suitable_balance


def test_invalid_high_suitable() -> None:
    weight = vos.Weight(kilograms=151)

    with raises(vos.WaterBalance.ExtremeWeightForSuitableWaterBalanceError):
        vos.WaterBalance.suitable_when(weight=weight)


def test_invalid_low_suitable() -> None:
    weight = vos.Weight(kilograms=29)

    with raises(vos.WaterBalance.ExtremeWeightForSuitableWaterBalanceError):
        vos.WaterBalance.suitable_when(weight=weight)


def test_identity_status() -> None:
    balance = vos.WaterBalance(water=vos.Water(milliliters=2000))
    assert balance.status_when(target=balance) is vos.WaterBalance.Status.good


def test_excess_water_status() -> None:
    balance = vos.WaterBalance(water=vos.Water(milliliters=2000))
    target = vos.WaterBalance(water=vos.Water(milliliters=1849))
    status = balance.status_when(target=target)

    assert status is vos.WaterBalance.Status.excess_water


def test_not_enough_water_status() -> None:
    balance = vos.WaterBalance(water=vos.Water(milliliters=2000))
    target = vos.WaterBalance(water=vos.Water(milliliters=2151))
    status = balance.status_when(target=target)

    assert status is vos.WaterBalance.Status.not_enough_water
