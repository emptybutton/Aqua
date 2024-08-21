from datetime import UTC

from dirty_equals import IsNow
from pytest import raises

from aqua.domain import entities, value_objects as vos


def test_user_creation_without_weight_and_target() -> None:
    with raises(entities.User.NoWeightForSuitableWaterBalanceError):
        entities.User(glass=vos.Glass(capacity=vos.Water(milliliters=200)))


def test_user_writing_without_water() -> None:
    weight = vos.Weight(kilograms=70)
    glass = vos.Glass(capacity=vos.Water(milliliters=200))
    user = entities.User(weight=weight, glass=glass)

    record = user.write_water()

    assert record.user_id == user.id
    assert record.drunk_water == user.glass.capacity
    assert record.recording_time == IsNow(tz=UTC)


def test_user_writing_with_water() -> None:
    water = vos.Water(milliliters=1000)
    weight = vos.Weight(kilograms=70)
    glass = vos.Glass(capacity=vos.Water(milliliters=200))
    user = entities.User(weight=weight, glass=glass)

    record = user.write_water(water)

    assert record.user_id == user.id
    assert record.drunk_water == water
    assert record.recording_time == IsNow(tz=UTC)


def test_user_creation_without_target() -> None:
    weight = vos.Weight(kilograms=70)
    glass = vos.Glass(capacity=vos.Water(milliliters=200))

    user = entities.User(weight=weight, glass=glass)

    assert user.target == user.suitable_water_balance


def test_user_creation_without_target_and_weight() -> None:
    glass = vos.Glass(capacity=vos.Water(milliliters=200))

    with raises(entities.User.NoWeightForSuitableWaterBalanceError):
        entities.User(glass=glass)


def test_user_creation_without_target_with_extreme_low_weight() -> None:
    weight = vos.Weight(kilograms=29)
    glass = vos.Glass(capacity=vos.Water(milliliters=200))

    with raises(vos.WaterBalance.ExtremeWeightForSuitableWaterBalanceError):
        entities.User(weight=weight, glass=glass)


def test_user_creation_without_target_with_extreme_high_weight() -> None:
    weight = vos.Weight(kilograms=151)
    glass = vos.Glass(capacity=vos.Water(milliliters=200))

    with raises(vos.WaterBalance.ExtremeWeightForSuitableWaterBalanceError):
        entities.User(weight=weight, glass=glass)


def test_user_suitable_water_balance_with_extreme_low_weight() -> None:
    weight = vos.Weight(kilograms=29)
    glass = vos.Glass(capacity=vos.Water(milliliters=200))
    target = vos.WaterBalance(water=vos.Water(milliliters=2000))

    user = entities.User(_target=target, weight=weight, glass=glass)

    with raises(vos.WaterBalance.ExtremeWeightForSuitableWaterBalanceError):
        user.suitable_water_balance  # noqa: B018


def test_user_suitable_water_balance_with_extreme_high_weight() -> None:
    weight = vos.Weight(kilograms=151)
    glass = vos.Glass(capacity=vos.Water(milliliters=200))
    target = vos.WaterBalance(water=vos.Water(milliliters=2000))

    user = entities.User(_target=target, weight=weight, glass=glass)

    with raises(vos.WaterBalance.ExtremeWeightForSuitableWaterBalanceError):
        user.suitable_water_balance  # noqa: B018


def test_user_suitable_water_balance_without_weight() -> None:
    target = vos.WaterBalance(water=vos.Water(milliliters=5000))
    glass = vos.Glass(capacity=vos.Water(milliliters=200))

    user = entities.User(glass=glass, _target=target)

    with raises(entities.User.NoWeightForSuitableWaterBalanceError):
        user.suitable_water_balance  # noqa: B018


def test_user_suitable_water_balance_with_target() -> None:
    suitable_water_balance = vos.WaterBalance(water=vos.Water(milliliters=2000))
    target = vos.WaterBalance(water=vos.Water(milliliters=5000))
    weight = vos.Weight(kilograms=70)
    glass = vos.Glass(capacity=vos.Water(milliliters=200))

    user = entities.User(_target=target, weight=weight, glass=glass)

    assert target == user.target
    assert user.target != user.suitable_water_balance
    assert user.suitable_water_balance == suitable_water_balance
