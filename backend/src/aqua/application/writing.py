from typing import Optional, Callable, TypeVar

from src.aqua.domain import entities, value_objects
from src.aqua.application import errors
from src.aqua.application.ports import repos
from src.shared.application.ports import uows


class BaseError(Exception): ...


class NoUser(BaseError): ...


class NoMilligrams(BaseError): ...


_RecordsT = TypeVar("_RecordsT", bound=repos.Records)
_UsersT = TypeVar("_UsersT", bound=repos.Users)


async def write_water(
    user_id: int,
    milligrams: Optional[int],
    *,
    users: repos.Users,
    records: _RecordsT,
    uow_for: Callable[[_RecordsT], uows.UoW[entities.Record]],
) -> entities.Record:
    user = await users.get_by_id(user_id)

    if user is None:
        raise errors.NoUser()

    if milligrams is not None:
        water = value_objects.Water(milligrams)
    else:
        if user.glass is None:
            raise errors.NoMilligrams()

        water = user.glass

    record = entities.Record(water, user.id)

    async with uow_for(records) as uow:
        uow.register_new(record)
        await records.add(record)

    return record
