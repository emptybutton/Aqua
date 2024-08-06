from typing import Optional, TypeVar
from uuid import UUID

from aqua.domain import entities, value_objects as vos
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
        water = vos.Water(milliliters=water_balance_milliliters)
        target = vos.WaterBalance(water=water)
    else:
        target = None

    if weight_kilograms is not None:
        weight = vos.Weight(kilograms=weight_kilograms)
    else:
        weight = None

    if glass_milliliters is None:
        glass_milliliters = 200

    glass = vos.Glass(capacity=vos.Water(milliliters=glass_milliliters))
    user = entities.User(
        id=user_id,
        glass=glass,
        weight=weight,
        _target=target,
    )

    async with uow_for(users) as uow:
        uow.register_new(user)
        await users.add(user)

    return user
