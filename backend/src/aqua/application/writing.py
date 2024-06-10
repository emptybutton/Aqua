from datetime import datetime, UTC
from typing import Optional, Callable, TypeVar

from src.aqua.domain import entities, value_objects
from src.aqua.application.ports import repos
from src.shared.application.ports import uows


class BaseError(Exception): ...


class NoUserError(BaseError): ...


_RecordsT = TypeVar("_RecordsT", bound=repos.Records)
_UsersT = TypeVar("_UsersT", bound=repos.Users)
_DaysT = TypeVar("_DaysT", bound=repos.Days)

async def write_water(  # noqa: PLR0913
    user_id: int,
    milliliters: Optional[int],
    *,
    users: repos.Users,
    records: _RecordsT,
    days: _DaysT,
    record_uow_for: Callable[[_RecordsT], uows.UoW[entities.Record]],
    day_uow_for: Callable[[_DaysT], uows.UoW[entities.Day]],
) -> entities.Record:
    user = await users.get_by_id(user_id)

    if user is None:
        raise NoUserError()

    water = None if milliliters is None else value_objects.Water(milliliters)

    record = user.write_water(water)

    record_uow = record_uow_for(records)
    day_uow = day_uow_for(days)

    async with record_uow as record_uow, day_uow as day_uow:
        record_uow.register_new(record)
        await records.add(record)

        day = await days.get_on(datetime.now(UTC).date())

        if day is None:
            day = entities.Day(
                date_=datetime.now(UTC).date(),
                user_id=user_id,
                target_water_balance=user.target_water_balance,
                __real_water_balance=value_objects.WaterBalance(
                    record.drunk_water,
                ),
            )
            day_uow.register_new(day)
            await days.add(day)
        else:
            water = day.real_water_balance.water + record.drunk_water
            day.real_water_balance = value_objects.WaterBalance(water)
            day_uow.register_dirty(day)

    return record
