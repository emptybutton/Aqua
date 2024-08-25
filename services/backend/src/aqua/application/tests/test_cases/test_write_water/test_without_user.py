from uuid import uuid4

from pytest import mark, raises

from aqua.application.cases import write_water
from aqua.application.tests import adapters
from aqua.domain import entities
from shared.application.tests.adapters.transactions import UoWTransactionFactory


@mark.asyncio
async def test_empty_storage() -> None:
    users = adapters.repos.InMemoryUsers()
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    transaction_factory = UoWTransactionFactory()
    logger = adapters.loggers.SavingLogger()

    with raises(write_water.NoUserError):
        await write_water.perform(
            user_id=uuid4(),
            milliliters=None,
            users=users,
            records=records,
            days=days,
            record_transaction_for=transaction_factory,
            day_transaction_for=transaction_factory,
            user_transaction_for=transaction_factory,
            logger=logger,
        )


@mark.asyncio
async def test_full_storage(user1: entities.User) -> None:
    users = adapters.repos.InMemoryUsers([user1])
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    transaction_factory = UoWTransactionFactory()
    logger = adapters.loggers.SavingLogger()

    with raises(write_water.NoUserError):
        await write_water.perform(
            user_id=uuid4(),
            milliliters=None,
            users=users,
            records=records,
            days=days,
            record_transaction_for=transaction_factory,
            day_transaction_for=transaction_factory,
            user_transaction_for=transaction_factory,
            logger=logger,
        )
