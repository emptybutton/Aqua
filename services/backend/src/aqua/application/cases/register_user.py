from typing import TypeVar
from uuid import UUID

from aqua.domain import entities, value_objects as vos
from aqua.application.ports import repos, loggers
from shared.application.ports.transactions import TransactionFactory


_UsersT = TypeVar("_UsersT", bound=repos.Users)


async def perform(
    user_id: UUID,
    water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
    *,
    users: _UsersT,
    transaction_for: TransactionFactory[_UsersT],
    logger: loggers.Logger,
) -> entities.User:
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

    async with transaction_for(users):
        user = await users.find_with_id(user_id)

        if user is not None:
            await logger.log_registered_user_registration(user)
            return user

        user = entities.User(
            id=user_id,
            glass=glass,
            weight=weight,
            _target=target,
        )

        await users.add(user)
        await logger.log_registered_user(user)

    return user
