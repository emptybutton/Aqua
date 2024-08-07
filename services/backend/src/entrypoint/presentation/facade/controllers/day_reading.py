from datetime import date
from typing import TypeAlias

from entrypoint.application.cases import day_reading
from entrypoint.infrastructure.adapters import gateways
from shared.infrastructure.adapters import uows
from shared.infrastructure.db.sessions import postgres_session_factory


OutputDTO: TypeAlias = day_reading.OutputDTO


async def read_day(
    jwt: str,
    date_: date,
) -> OutputDTO:
    async with postgres_session_factory() as session:
        return await day_reading.read_day(
            jwt,
            date_,
            uow=uows.DBUoW(session),
            auth_gateway=gateways.AuthGateway(),
            aqua_gateway=gateways.AquaGateway(),
        )
