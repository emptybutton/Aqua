from dataclasses import dataclass
from datetime import datetime, UTC
from typing import TypeVar
from uuid import UUID

from aqua.domain import entities, value_objects as vos
from aqua.application.ports import repos, loggers
from shared.application.ports.transactions import TransactionFactory


@dataclass(kw_only=True)
class Output:
    new_record: entities.Record
    previous_records: tuple[entities.Record, ...]
    day: entities.Day
    user: entities.User


class Error(Exception): ...


class NoUserError(Error): ...


_UsersT = TypeVar("_UsersT", bound=repos.Users)
_RecordsT = TypeVar("_RecordsT", bound=repos.Records)
_DaysT = TypeVar("_DaysT", bound=repos.Days)


async def perform(
    user_id: UUID,
    milliliters: int | None,
    *,
    users: _UsersT,
    records: _RecordsT,
    days: _DaysT,
    record_transaction_for: TransactionFactory[_RecordsT],
    day_transaction_for: TransactionFactory[_DaysT],
    user_transaction_for: TransactionFactory[_UsersT],
    logger: loggers.Logger,
) -> Output:
    water = None if milliliters is None else vos.Water(milliliters=milliliters)
    today = datetime.now(UTC).date()

    async with user_transaction_for(users):
        user = await users.find_with_id(user_id)

        if user is None:
            raise NoUserError()

        new_record = user.write_water(water)

        async with record_transaction_for(records), day_transaction_for(days):
            previous_records = await records.find_from(today, user_id=user_id)

            await records.add(new_record)

            if len(previous_records) == 0:
                day = entities.Day.empty_of(user, date_=today)
                day.add(new_record)
                await days.add(day)
                await logger.log_new_day(day)
            else:
                found_day = await days.find_from(today, user_id=user.id)

                if found_day is not None:
                    day = found_day
                    day.add(new_record)
                    await days.update(day)
                    await logger.log_new_day_state(day)
                else:
                    for record in previous_records:
                        await logger.log_record_without_day(record)

                    day = entities.Day.empty_of(user, date_=today)
                    day.add(new_record)
                    await days.add(day)
                    await logger.log_new_day(day)

            await logger.log_new_record(new_record)

    return Output(
        previous_records=previous_records,
        new_record=new_record,
        day=day,
        user=user,
    )
