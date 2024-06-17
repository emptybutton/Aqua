from typing import Optional, TypeAlias

from src.entrypoint.application import registration
from src.entrypoint.infrastructure.adapters import gateways
from src.shared.infrastructure.adapters import uows
from src.shared.infrastructure.db.sessions import postgres_session_factory


OutputDTO: TypeAlias = registration.OutputDTO


async def register_user(
    name: str,
    password: str,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
) -> OutputDTO:
    async with postgres_session_factory() as session:
        return await registration.register_user(
            name,
            password,
            water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            uow=uows.DBUoW(session),
            register_auth_user=gateways.register_auth_user,
            register_aqua_user=gateways.register_aqua_user,
        )
