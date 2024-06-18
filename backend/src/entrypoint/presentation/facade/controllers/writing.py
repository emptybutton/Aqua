from typing import Optional, TypeAlias

from src.entrypoint.application.cases import writing
from src.entrypoint.infrastructure.adapters import gateways
from src.shared.infrastructure.adapters import uows
from src.shared.infrastructure.db.sessions import postgres_session_factory


OutputDTO: TypeAlias = writing.OutputDTO


async def write_water(
    jwt: str,
    milliliters: Optional[int],
) -> OutputDTO:
    async with postgres_session_factory() as session:
        return await writing.write_water(
            jwt,
            milliliters,
            auth_gateway=gateways.AuthGateway(),
            aqua_gateway=gateways.AquaGateway(),
            uow=uows.DBUoW(session),
        )
