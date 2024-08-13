from dataclasses import dataclass
from datetime import datetime, date
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application.cases import read_day_records
from entrypoint.application import ports
from entrypoint.infrastructure import adapters
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    @dataclass(kw_only=True, frozen=True)
    class RecordData:
        id: UUID
        drunk_water: int
        recording_time: datetime

    records: tuple[RecordData, ...]


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_access_token"]
    | Literal["no_user"]
)


async def perform(jwt: str, date_: date) -> Output:
    async with async_container() as container:
        result = await read_day_records.perform(
            jwt,
            date_,
            transaction=await container.get(DBTransaction),
            auth=await container.get(adapters.clients.AuthFacade),
            aqua=await container.get(adapters.clients.AquaFacade),
            auth_logger=await container.get(adapters.loggers.AuthFacadeLogger),
            aqua_logger=await container.get(adapters.loggers.AquaFacadeLogger),
        )

    if not isinstance(result, ports.clients.aqua.ReadDayRecordsOutput):
        return result

    return OutputData(records=tuple(
        OutputData.RecordData(
            id=record.id,
            drunk_water=record.drunk_water,
            recording_time=record.recording_time,
        )
        for record in result.records
    ))
