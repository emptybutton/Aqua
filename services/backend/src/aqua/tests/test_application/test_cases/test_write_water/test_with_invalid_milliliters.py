from uuid import uuid4

from pytest import mark, raises

from aqua.application.cases import write_water
from aqua.domain import value_objects as vos
from aqua.infrastructure import adapters
from shared.infrastructure.adapters.transactions import (
    InMemoryUoWTransactionFactory,
)


@mark.asyncio
async def test() -> None:
    users = adapters.repos.InMemoryUsers()
    records = adapters.repos.InMemoryRecords()
    days = adapters.repos.InMemoryDays()
    transaction_factory = InMemoryUoWTransactionFactory()
    logger = adapters.loggers.InMemoryStorageLogger()

    with raises(vos.Water.IncorrectAmountError):
        await write_water.perform(
            user_id=uuid4(),
            milliliters=-500,
            users=users,
            records=records,
            days=days,
            record_transaction_for=transaction_factory,
            day_transaction_for=transaction_factory,
            user_transaction_for=transaction_factory,
            logger=logger,
        )
