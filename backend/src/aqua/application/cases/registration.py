from typing import Optional, TypeVar
from uuid import UUID

from aqua.domain import entities, value_objects
from aqua.application.ports import repos
from shared.application.ports import uows


_UsersT = TypeVar("_UsersT", bound=repos.Users)


async def register_user(  # noqa: PLR0913
    user_id: UUID,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
    *,
    users: _UsersT,
    uow_for: uows.UoWFactory[_UsersT, entities.User],
) -> entities.User:
    user = await users.get_by_id(user_id)

    if user is not None:
        return user

    if water_balance_milliliters is not None:
        water = value_objects.Water(water_balance_milliliters)
        water_balance = value_objects.WaterBalance(water)
    else:
        water_balance = None

    if weight_kilograms is not None:
        weight = value_objects.Weight(weight_kilograms)
    else:
        weight = None

    if glass_milliliters is None:
        glass_milliliters = 200

    glass = value_objects.Glass(value_objects.Water(glass_milliliters))
    user = entities.User(glass, weight, water_balance, user_id)

    async with uow_for(users) as uow:
        uow.register_new(user)
        await users.add(user)

    return user
