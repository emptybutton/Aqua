from datetime import UTC, datetime

from dirty_equals import IsNow
from pytest import mark

from aqua.application.cases import write_water
from aqua.domain import entities, value_objects as vos
from aqua.infrastructure import adapters
from shared.infrastructure.adapters.transactions import (
    InMemoryUoWTransactionFactory,
)


@mark.asyncio
async def test_result(user1: entities.User) -> None:
    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    transaction_factory = InMemoryUoWTransactionFactory()
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await write_water.perform(
        user_id=user1.id,
        milliliters=None,
        users=users,
        records=records,
        days=days,
        record_transaction_for=transaction_factory,
        day_transaction_for=transaction_factory,
        user_transaction_for=transaction_factory,
        logger=logger,
    )

    assert result.new_record.user_id == user1.id
    assert result.new_record.drunk_water == vos.Water(milliliters=300)
    assert result.new_record.recording_time == IsNow(tz=UTC)
    assert result.previous_records == tuple()
    assert result.user == user1
    assert result.day.user_id == user1.id
    assert result.day.date_ == datetime.now(UTC).date()
    assert result.day.target == user1.target
    assert result.day.water_balance == vos.WaterBalance(
        water=vos.Water(milliliters=300),
    )
    assert result.day.result is vos.WaterBalance.Status.not_enough_water
    assert not result.day.is_result_pinned


@mark.asyncio
async def test_storage_values(user1: entities.User) -> None:
    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    transaction_factory = InMemoryUoWTransactionFactory()
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await write_water.perform(
        user_id=user1.id,
        milliliters=None,
        users=users,
        records=records,
        days=days,
        record_transaction_for=transaction_factory,
        day_transaction_for=transaction_factory,
        user_transaction_for=transaction_factory,
        logger=logger,
    )

    assert users[0] == result.user
    assert days[0] == result.day
    assert records[0] == result.new_record


@mark.asyncio
async def test_storage_sizes(user1: entities.User) -> None:
    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    transaction_factory = InMemoryUoWTransactionFactory()
    logger = adapters.loggers.InMemoryStorageLogger()

    await write_water.perform(
        user_id=user1.id,
        milliliters=None,
        users=users,
        records=records,
        days=days,
        record_transaction_for=transaction_factory,
        day_transaction_for=transaction_factory,
        user_transaction_for=transaction_factory,
        logger=logger,
    )

    assert len(users) == 1
    assert len(days) == 1
    assert len(records) == 1


@mark.asyncio
async def test_logger_values(user1: entities.User) -> None:
    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    transaction_factory = InMemoryUoWTransactionFactory()
    logger = adapters.loggers.InMemoryStorageLogger()

    result = await write_water.perform(
        user_id=user1.id,
        milliliters=None,
        users=users,
        records=records,
        days=days,
        record_transaction_for=transaction_factory,
        day_transaction_for=transaction_factory,
        user_transaction_for=transaction_factory,
        logger=logger,
    )

    assert logger.new_days[0] == result.day
    assert logger.new_records[0] == result.new_record


@mark.asyncio
async def test_logger_size(user1: entities.User) -> None:
    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    transaction_factory = InMemoryUoWTransactionFactory()
    logger = adapters.loggers.InMemoryStorageLogger()

    await write_water.perform(
        user_id=user1.id,
        milliliters=None,
        users=users,
        records=records,
        days=days,
        record_transaction_for=transaction_factory,
        day_transaction_for=transaction_factory,
        user_transaction_for=transaction_factory,
        logger=logger,
    )

    assert len(logger.new_days) == 1
    assert len(logger.new_records) == 1
