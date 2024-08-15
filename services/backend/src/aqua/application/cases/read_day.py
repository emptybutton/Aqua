from uuid import UUID
from dataclasses import dataclass
from datetime import date

from aqua.domain import entities
from aqua.application.ports import repos


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
) -> Output:
    user = await users.find_with_id(user_id)

    if user is None:
        raise NoUserError()

    day = await days.find_from(date_, user_id=user.id)
    found_records = await records.find_from(date_, user_id=user.id)

    if day is None:
        day = entities.Day(user_id=user.id, target=user.target)

    return Output(user=user, day=day, records=found_records)
