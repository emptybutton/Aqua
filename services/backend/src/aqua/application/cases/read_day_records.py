from datetime import date
from uuid import UUID

from aqua.domain import entities
from aqua.application.ports import repos


class Error(Exception): ...


class NoUserError(Error): ...


async def perform(
    user_id: UUID,
    date_: date,
    *,
    users: repos.Users,
    records: repos.Records,
) -> tuple[entities.Record, ...]:
    if not await users.contains_with_id(user_id):
        raise NoUserError()

    return await records.find_from(date_, user_id=user_id)
