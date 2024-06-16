from datetime import date

from src.aqua.domain import entities
from src.aqua.application.ports import repos


class BaseError(Exception): ...


class NoUserError(BaseError): ...


async def read_day_records(
    user_id: int,
    date_: date,
    *,
    users: repos.Users,
    records: repos.Records,
) -> tuple[entities.Record, ...]:
    if not await users.has_with_id(user_id):
        raise NoUserError()

    return await records.get_on(date_, user_id=user_id)
