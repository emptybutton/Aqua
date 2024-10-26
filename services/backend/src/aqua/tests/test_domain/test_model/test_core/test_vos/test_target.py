from aqua.domain.model.core.vos.target import Result, Target, result_of
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.water import Water


def test_identity_result() -> None:
    water_balance = WaterBalance(water=Water.with_(milliliters=2000).unwrap())
    target = Target(water_balance=water_balance)

    result = result_of(target, water_balance=target.water_balance)

    assert result is Result.good


def test_excess_water_status() -> None:
    target = Target(
        water_balance=WaterBalance(water=Water.with_(milliliters=1849).unwrap())
    )
    water_balance = WaterBalance(water=Water.with_(milliliters=2000).unwrap())

    result = result_of(target, water_balance=water_balance)

    assert result is Result.excess_water


def test_not_enough_water_status() -> None:
    target = Target(
        water_balance=WaterBalance(water=Water.with_(milliliters=2151).unwrap())
    )
    water_balance = WaterBalance(water=Water.with_(milliliters=2000).unwrap())

    result = result_of(target, water_balance=water_balance)

    assert result is Result.not_enough_water
