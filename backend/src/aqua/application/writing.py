from typing import Optional, Callable, TypeVar

from src.aqua.domain import entities, value_objects
from src.aqua.application.ports import repos
from src.shared.application.ports import uows


class BaseError(Exception): ...


class NoUserError(BaseError): ...


_TodayRecordsT = TypeVar("_TodayRecordsT", bound=repos.TodayRecords)
_UsersWithTodayRecordsT = TypeVar(
    "_UsersWithTodayRecordsT",
    bound=repos.UsersWithTodayRecords,
)


async def write_water(  # noqa: PLR0913
    user_id: int,
    milliliters: Optional[int],
    *,
    users: repos.Users,
    users_with_today_records: _UsersWithTodayRecordsT,
    today_records: _TodayRecordsT,
    record_uow_for: Callable[[_TodayRecordsT], uows.UoW[entities.Record]],
    user_uow_for: Callable[[_UsersWithTodayRecordsT], uows.UoW[entities.User]],
) -> entities.Record:
    user = await users.get_by_id(user_id)

    if user is None:
        raise NoUserError()

    water = None if milliliters is None else value_objects.Water(milliliters)
    record = user.write_water(water)

    record_uow = record_uow_for(today_records)
    user_uow = user_uow_for(users_with_today_records)

    async with record_uow, user_uow:
        record_uow.register_new(record)
        await today_records.add(record)

        user_uow.register_new(user)
        await users_with_today_records.add(user)

    return record
