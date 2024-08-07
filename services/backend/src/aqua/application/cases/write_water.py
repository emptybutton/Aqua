from dataclasses import dataclass
from datetime import datetime, UTC
from typing import TypeVar
from uuid import UUID

from aqua.domain import entities, value_objects as vos
from aqua.application.ports import repos
from shared.application.ports.transactions import TransactionFactory


@dataclass(kw_only=True)
class Output:
    record: entities.Record
    day: entities.Day
    user: entities.User


class Error(Exception): ...


class NoUserError(Error): ...


_UsersT = TypeVar("_UsersT", bound=repos.Users)
_RecordsT = TypeVar("_RecordsT", bound=repos.Records)
_DaysT = TypeVar("_DaysT", bound=repos.Days)


async def perform(  # noqa: PLR0913
    user_id: UUID,
    milliliters: int | None,
    *,
    users: _UsersT,
    records: _RecordsT,
    days: _DaysT,
    record_transaction_for: TransactionFactory[_RecordsT],
    day_transaction_for: TransactionFactory[_DaysT],
    user_transaction_for: TransactionFactory[_UsersT],
) -> Output:
    water = None if milliliters is None else vos.Water(milliliters=milliliters)

    async with user_transaction_for(users):
        user = await users.find_with_id(user_id)

        if user is None:
            raise NoUserError()

        record = user.write_water(water)

        async with record_transaction_for(records), day_transaction_for(days):
            await records.add(record)

            today = datetime.now(UTC).date()
            day = await days.find_from(today, user_id=user.id)

            if day is None:
                day = entities.Day(
                    user_id=user_id,
                    target=user.target,
                    _water_balance=vos.WaterBalance(water=record.drunk_water),
                )
                await days.add(day)
            else:
                day.add(record)
                await days.update(day)

    return Output(record=record, day=day, user=user)
