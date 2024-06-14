from datetime import datetime, UTC, date

from src.aqua.domain import entities
from src.aqua.application.ports import repos


class BaseError(Exception): ...


class NoUserError(BaseError): ...


async def read_day_records(
    user_id: int,
    date_: date,
    *,
    users: repos.Users,
    today_records: repos.TodayRecords,
    past_records: repos.PastRecords,
) -> tuple[entities.Record, ...]:
    if not await users.has_with_id(user_id):
        raise NoUserError()

    current_date = datetime.now(UTC).date()

    if date_ == current_date:
        return await today_records.get_all_with_user_id(user_id)

    if date_ > current_date:
        return tuple()

    return await past_records.get_on(date_, user_id=user_id)
