from datetime import UTC, datetime
from uuid import uuid4

from aqua.domain import entities
from aqua.domain import value_objects as vos


def test_day_correct_result_without_water_balance() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
    )

    assert day.result is day.correct_result


def test_day_correct_result_with_water_balance() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=50)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=25_000)),
    )

    assert day.result is day.correct_result


def test_day_not_enough_water_result() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=1849)),
    )

    assert day.result is vos.WaterBalance.Status.not_enough_water
    assert day.correct_result is vos.WaterBalance.Status.not_enough_water


def test_day_excess_water_result() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=2151)),
    )

    assert day.result is vos.WaterBalance.Status.excess_water
    assert day.correct_result is vos.WaterBalance.Status.excess_water


def test_day_good_result_by_upper_limit() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=2150)),
    )

    assert day.result is vos.WaterBalance.Status.good
    assert day.correct_result is vos.WaterBalance.Status.good


def test_day_good_result_by_lower_limit() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=1850)),
    )

    assert day.result is vos.WaterBalance.Status.good
    assert day.correct_result is vos.WaterBalance.Status.good


def test_day_good_result_when_target_is_fully_accomplished() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=2000)),
    )

    assert day.result is vos.WaterBalance.Status.good
    assert day.correct_result is vos.WaterBalance.Status.good


def test_is_result_pinned_with_result() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=5)),
        _result=vos.WaterBalance.Status.good,
    )

    assert day.result is vos.WaterBalance.Status.good
    assert day.correct_result is vos.WaterBalance.Status.not_enough_water
    assert day.is_result_pinned


def test_is_result_pinned_without_result() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=5)),
    )

    assert day.result is vos.WaterBalance.Status.not_enough_water
    assert day.correct_result is vos.WaterBalance.Status.not_enough_water
    assert not day.is_result_pinned


def test_is_result_pinned_with_result_setting() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=5)),
    )

    day.result = vos.WaterBalance.Status.good

    assert day.result is vos.WaterBalance.Status.good
    assert day.correct_result is vos.WaterBalance.Status.not_enough_water
    assert day.is_result_pinned


def test_is_result_pinned_with_is_result_pinned_enabling() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=5)),
    )

    day.is_result_pinned = True

    assert day.result is vos.WaterBalance.Status.not_enough_water
    assert day.correct_result is vos.WaterBalance.Status.not_enough_water
    assert day.is_result_pinned


def test_is_result_pinned_with_is_result_pinned_disabling_and_result() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=5)),
        _result=vos.WaterBalance.Status.good,
    )

    day.is_result_pinned = False

    assert day.result is vos.WaterBalance.Status.not_enough_water
    assert day.correct_result is vos.WaterBalance.Status.not_enough_water
    assert not day.is_result_pinned


def test_is_result_pinned_with_result_and_water_balance_setting() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=5)),
        _result=vos.WaterBalance.Status.good,
    )

    day.water_balance = vos.WaterBalance(water=vos.Water(milliliters=50_000))

    assert day.result is vos.WaterBalance.Status.good
    assert day.correct_result is vos.WaterBalance.Status.excess_water
    assert day.is_result_pinned


def test_is_result_pinned_with_water_balance_setting() -> None:
    day = entities.Day(
        user_id=uuid4(),
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=5)),
    )

    day.water_balance = vos.WaterBalance(water=vos.Water(milliliters=50_000))

    assert day.result is vos.WaterBalance.Status.excess_water
    assert day.correct_result is vos.WaterBalance.Status.excess_water
    assert not day.is_result_pinned


def test_take_into_consideration_record() -> None:
    user_id = uuid4()
    record = entities.Record(
        user_id=user_id, drunk_water=vos.Water(milliliters=5050)
    )
    day = entities.Day(
        user_id=user_id,
        target=vos.WaterBalance(water=vos.Water(milliliters=2000)),
        _water_balance=vos.WaterBalance(water=vos.Water(milliliters=505)),
    )
    expected_water_balance = vos.WaterBalance(water=vos.Water(milliliters=5555))

    day.take_into_consideration(record)

    assert day.water_balance == expected_water_balance


def test_empty_day_target() -> None:
    target = vos.WaterBalance(water=vos.Water(milliliters=1000))
    glass = vos.Glass(capacity=vos.Water(milliliters=200))
    user = entities.User(glass=glass, _target=target)
    today = datetime.now(UTC)

    day = entities.Day.empty_of(user, date_=today)

    assert day.target == user.target


def test_empty_day_water_balance() -> None:
    target = vos.WaterBalance(water=vos.Water(milliliters=1000))
    glass = vos.Glass(capacity=vos.Water(milliliters=200))
    user = entities.User(glass=glass, _target=target)
    today = datetime.now(UTC)

    day = entities.Day.empty_of(user, date_=today)

    assert day.water_balance == vos.WaterBalance(water=vos.Water(milliliters=0))
