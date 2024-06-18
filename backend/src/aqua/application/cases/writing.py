from datetime import datetime, UTC
from typing import Optional, TypeVar
from uuid import UUID

from src.aqua.domain import entities, value_objects
from src.aqua.application.ports import repos
from src.shared.application.ports import uows


class BaseError(Exception): ...


class NoUserError(BaseError): ...


_RecordsT = TypeVar("_RecordsT", bound=repos.Records)
_DaysT = TypeVar("_DaysT", bound=repos.Days)


async def write_water(  # noqa: PLR0913
    user_id: UUID,
    milliliters: Optional[int],
    *,
    users: repos.Users,
    records: _RecordsT,
    days: _DaysT,
    record_uow_for: uows.UoWFactory[_RecordsT, entities.Record],
    day_uow_for: uows.UoWFactory[_DaysT, entities.Day],
) -> entities.Record:
    user = await users.get_by_id(user_id)

    if user is None:
        raise NoUserError()

    water = None if milliliters is None else value_objects.Water(milliliters)
    record = user.write_water(water)

    record_uow = record_uow_for(records)
    day_uow = day_uow_for(days)

    async with record_uow, day_uow:
        record_uow.register_new(record)
        await records.add(record)

        day = await days.get_on(datetime.now(UTC).date(), user_id=user.id)

        if day is None:
            day = entities.Day(
                user_id=user_id,
                target_water_balance=user.target_water_balance,
                _real_water_balance=value_objects.WaterBalance(
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
