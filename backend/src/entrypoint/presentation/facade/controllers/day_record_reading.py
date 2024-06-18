from datetime import date
from typing import TypeAlias

from src.entrypoint.application.cases import day_record_reading
from src.entrypoint.infrastructure.adapters import gateways
from src.shared.infrastructure.adapters import uows
from src.shared.infrastructure.db.sessions import postgres_session_factory


OutputDTO: TypeAlias = day_record_reading.OutputDTO

RecordDTO: TypeAlias = day_record_reading.RecordDTO


async def read_day_records(
    jwt: str,
    date_: date,
) -> OutputDTO:
    async with postgres_session_factory() as session:
        return await day_record_reading.read_day_records(
            jwt,
            date_,
            uow=uows.DBUoW(session),
            auth_gateway=gateways.AuthGateway(),
            aqua_gateway=gateways.AquaGateway(),
        )
