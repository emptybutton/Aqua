from typing import Optional, TypeAlias
from functools import partial

from sqlalchemy.ext.asyncio import AsyncEngine

from src.entrypoint.application import registration
from src.entrypoint.infrastructure.adapters import actions
from src.shared.infrastructure.adapters import uows


OutputDTO: TypeAlias = registration.OutputDTO


async def register_user(  # noqa: PLR0913
    name: str,
    password: str,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
    *,
    engine: AsyncEngine,
) -> OutputDTO:
    connection = engine.connect()

    register_auth_user = partial(
        actions.register_auth_user,
        connection=connection,
    )

    register_aqua_user = partial(
        actions.register_auth_user,
        connection=connection,
    )

    return await registration.register_user(
        name,
        password,
        water_balance_milliliters,
        glass_milliliters,
        weight_kilograms,
        uow=uows.TransactionalUoW(connection, closes=True),
        register_auth_user=register_auth_user,
        register_aqua_user=register_aqua_user,
    )
