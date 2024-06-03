from typing import Optional, Callable, TypeVar

from src.aqua.domain import entities, value_objects
from src.aqua.application import errors
from src.aqua.application.ports import repos
from src.shared.application.ports import uows


_RecordsT = TypeVar("_RecordsT", bound=repos.Records)
_UsersT = TypeVar("_UsersT", bound=repos.Users)


async def register_user(  # noqa: PLR0913
    user_id: int,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
    *,
    users: _UsersT,
    uow_for: Callable[[_UsersT], uows.UoW[entities.User]],
) -> entities.User:
    user = await users.get_by_id(user_id)

    if user is not None:
        return user

    if water_balance_milliliters is not None:
        water_balance = value_objects.Water(water_balance_milliliters)
    else:
        water_balance = None

    if glass_milliliters is not None:
        glass = value_objects.Water(glass_milliliters)
    else:
        glass = None

    if weight_kilograms is not None:
        weight = value_objects.Weight(weight_kilograms)
    else:
        weight = None

    user = entities.User(weight, glass, water_balance)

    async with uow_for(users) as uow:
        uow.register_new(user)
        await users.add(user)

    return user


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
