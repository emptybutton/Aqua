from uuid import uuid4

from aqua.domain import entities, value_objects as vos


def test_water_balance_of_zero_records() -> None:
    zero_water_balance = vos.WaterBalance(water=vos.Water(milliliters=0))
    water_balance_of_zero_records = entities.water_balance_from()

    assert water_balance_of_zero_records == zero_water_balance


def test_water_balance_of_one_record() -> None:
    water = vos.Water(milliliters=2000)
    expected_water_balance = vos.WaterBalance(water=water)

    record = entities.Record(user_id=uuid4(), drunk_water=water)

    assert entities.water_balance_from(record) == expected_water_balance


def test_water_balance_of_many_records() -> None:
    expected_water_balance = vos.WaterBalance(water=vos.Water(milliliters=7777))

    water1 = vos.Water(milliliters=570)
    water2 = vos.Water(milliliters=200)
    water3 = vos.Water(milliliters=7007)

    record1 = entities.Record(user_id=uuid4(), drunk_water=water1)
    record2 = entities.Record(user_id=uuid4(), drunk_water=water2)
    record3 = entities.Record(user_id=uuid4(), drunk_water=water3)

    water_balance = entities.water_balance_from(record1, record2, record3)

    assert water_balance == expected_water_balance
