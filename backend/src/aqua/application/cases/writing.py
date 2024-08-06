from datetime import datetime, UTC
from typing import Optional, TypeVar
from uuid import UUID

from aqua.domain import entities, value_objects as vos
from aqua.application.ports import repos
from shared.application.ports import uows


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

    water = None if milliliters is None else vos.Water(milliliters=milliliters)
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
                target=user.target,
                _water_balance=vos.WaterBalance(water=record.drunk_water),
            )
            day_uow.register_new(day)
            await days.add(day)
        else:
            day.add(record)
            day_uow.register_dirty(day)

    return record
