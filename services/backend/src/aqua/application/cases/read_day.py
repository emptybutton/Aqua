from uuid import UUID
from dataclasses import dataclass
from datetime import date

from aqua.domain import entities
from aqua.application.ports import repos, loggers


@dataclass(kw_only=True, frozen=True)
class Output:
    user: entities.User
    day: entities.Day
    records: tuple[entities.Record, ...]


class Error(Exception): ...


class NoUserError(Error): ...


async def perform(
    user_id: UUID,
    date_: date,
    *,
    users: repos.Users,
    days: repos.Days,
    records: repos.Records,
    logger: loggers.Logger,
) -> Output:
    user = await users.find_with_id(user_id)

    if user is None:
        raise NoUserError()

    day = await days.find_from(date_, user_id=user.id)
    found_records = await records.find_from(date_, user_id=user.id)

    if day is None and len(found_records) != 0:
        await logger.log_records_without_day(found_records)

    if day is not None and len(found_records) == 0:
        await logger.log_day_without_records(day)

    if day is None:
        day = entities.Day.empty_of(user, date_=date_)

    return Output(user=user, day=day, records=found_records)
