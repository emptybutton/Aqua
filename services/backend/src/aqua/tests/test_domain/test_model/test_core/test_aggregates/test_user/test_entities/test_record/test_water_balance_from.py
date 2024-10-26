from datetime import UTC, datetime
from uuid import uuid4

from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
    water_balance_from,
)
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water


def test_zero_records() -> None:
    zero_water_balance = WaterBalance(water=Water.with_(milliliters=0).unwrap())

    water_balance_of_zero_records = water_balance_from()

    assert water_balance_of_zero_records == zero_water_balance


def test_one_record() -> None:
    water = Water.with_(milliliters=2000).unwrap()
    expected_water_balance = WaterBalance(water=water)

    record = Record(
        id=uuid4(),
        events=list(),
        user_id=uuid4(),
        drunk_water=water,
        recording_time=Time.with_(datetime_=datetime.now(UTC)).unwrap(),
        is_cancelled=False,
    )

    assert water_balance_from(record) == expected_water_balance


def test_many_records() -> None:
    water = Water.with_(milliliters=111).unwrap()
    expected_water_balance = WaterBalance(water=water)

    record1 = Record(
        id=uuid4(),
        events=list(),
        user_id=uuid4(),
        drunk_water=Water.with_(milliliters=1).unwrap(),
        recording_time=Time.with_(datetime_=datetime.now(UTC)).unwrap(),
        is_cancelled=False,
    )
    record2 = Record(
        id=uuid4(),
        events=list(),
        user_id=uuid4(),
        drunk_water=Water.with_(milliliters=10).unwrap(),
        recording_time=Time.with_(datetime_=datetime.now(UTC)).unwrap(),
        is_cancelled=False,
    )
    record3 = Record(
        id=uuid4(),
        events=list(),
        user_id=uuid4(),
        drunk_water=Water.with_(milliliters=100).unwrap(),
        recording_time=Time.with_(datetime_=datetime.now(UTC)).unwrap(),
        is_cancelled=False,
    )

    water_balance = water_balance_from(record1, record2, record3)

    assert water_balance == expected_water_balance
