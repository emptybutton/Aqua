from typing import Optional, TypeAlias

from src.entrypoint.application.cases import user_data_reading
from src.entrypoint.infrastructure.adapters import gateways
from src.shared.infrastructure.adapters import uows
from src.shared.infrastructure.db.sessions import postgres_session_factory


OutputDTO: TypeAlias = user_data_reading.OutputDTO


async def read_user_data(jwt: str) -> Optional[OutputDTO]:
    async with postgres_session_factory() as session:
        return await user_data_reading.read_user_data(
            jwt,
            uow=uows.DBUoW(session),
            auth_gateway=gateways.AuthGateway(),
            aqua_gateway=gateways.AquaGateway(),
        )
