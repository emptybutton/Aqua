from datetime import UTC, datetime
from uuid import UUID

from pytest import fixture, mark, raises

from aqua.application.cases import read_day
from aqua.domain import entities
from aqua.domain import value_objects as vos
from aqua.infrastructure import adapters


@fixture
def user1() -> entities.User:
    return entities.User(
        id=UUID(int=1),
        weight=vos.Weight(kilograms=70),
        glass=vos.Glass(capacity=vos.Water(milliliters=300)),
        _target=vos.WaterBalance(water=vos.Water(milliliters=5000)),
    )


@mark.asyncio
async def test_without_user(user1: entities.User) -> None:
    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    logger = adapters.loggers.InMemoryStorageLogger()

    with raises(read_day.NoUserError):
        await read_day.perform(
            UUID(int=100),
            datetime(2006, 1, 1, tzinfo=UTC),
            users=users,
            records=records,
            days=days,
            logger=logger,
        )

    assert logger.is_empty


@mark.asyncio
async def test_with_user(user1: entities.User) -> None:
    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    logger = adapters.loggers.InMemoryStorageLogger()
    date_ = datetime(2006, 1, 1, tzinfo=UTC).date()
    expected_day_water = vos.Water(milliliters=0)
    expected_day_water_balance = vos.WaterBalance(water=expected_day_water)

    result = await read_day.perform(
        user1.id, date_, users=users, records=records, days=days, logger=logger
    )

    assert result.user == user1
    assert result.records == tuple()
    assert result.day.user_id == user1.id
    assert result.day.date_ == date_
    assert result.day.target == user1.target
    assert result.day.water_balance == expected_day_water_balance
    assert logger.is_empty


@mark.asyncio
async def test_with_day(user1: entities.User) -> None:
    date_ = datetime(2006, 1, 1, tzinfo=UTC).date()
    day1 = entities.Day(
        id=UUID(int=500), user_id=user1.id, target=user1.target, date_=date_
    )

    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays([day1])
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await read_day.perform(
        user1.id, date_, users=users, records=records, days=days, logger=logger
    )

    assert result.user == user1
    assert result.records == tuple()
    assert result.day == day1
    assert logger.days_without_records[0] == day1


@mark.asyncio
async def test_with_day_and_records(user1: entities.User) -> None:
    recording_time = datetime(2006, 1, 1, tzinfo=UTC)
    recording_date = recording_time.date()

    day1 = entities.Day(
        id=UUID(int=500),
        user_id=user1.id,
        target=user1.target,
        date_=recording_date,
    )
    record1 = entities.Record(
        id=UUID(int=101),
        user_id=user1.id,
        drunk_water=vos.Water(milliliters=500),
        _recording_time=recording_time,
    )
    record2 = entities.Record(
        id=UUID(int=102),
        user_id=UUID(int=1000),
        drunk_water=vos.Water(milliliters=8000),
        _recording_time=recording_time,
    )

    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords([record1, record2])
    days = adapters.repos.InMemoryDays([day1])
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await read_day.perform(
        user1.id,
        recording_date,
        users=users,
        records=records,
        days=days,
        logger=logger,
    )

    assert result.user == user1
    assert result.records == (record1,)
    assert result.day == day1
    assert logger.is_empty


@mark.asyncio
async def test_with_records(user1: entities.User) -> None:
    recording_time = datetime(2006, 1, 1, tzinfo=UTC)
    recording_date = recording_time.date()
    record1 = entities.Record(
        id=UUID(int=101),
        user_id=user1.id,
        drunk_water=vos.Water(milliliters=500),
        _recording_time=recording_time,
    )
    record2 = entities.Record(
        id=UUID(int=102),
        user_id=UUID(int=1000),
        drunk_water=vos.Water(milliliters=8000),
        _recording_time=recording_time,
    )
    expected_day_water = vos.Water(milliliters=0)
    expected_day_water_balance = vos.WaterBalance(water=expected_day_water)

    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords([record1, record2])
    days = adapters.repos.InMemoryDays()
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await read_day.perform(
        user1.id,
        recording_date,
        users=users,
        records=records,
        days=days,
        logger=logger,
    )

    assert result.user == user1
    assert result.records == (record1,)
    assert result.day.user_id == user1.id
    assert result.day.date_ == recording_date
    assert result.day.target == user1.target
    assert result.day.water_balance == expected_day_water_balance
    assert logger.records_without_day[0] == record1
