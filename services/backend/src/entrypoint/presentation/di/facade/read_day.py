from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application.cases import read_day
from entrypoint.application import ports
from entrypoint.infrastructure import adapters
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    target_water_balance_milliliters: int
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool

    @dataclass(kw_only=True, frozen=True)
    class RecordData:
        record_id: UUID
        drunk_water_milliliters: int
        recording_time: datetime

    records: tuple[RecordData, ...]


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_jwt"]
    | Literal["no_user"]
)


async def perform(jwt: str, date_: date) -> Output:
    async with async_container() as container:
        result = await read_day.perform(
            jwt,
            date_,
            transaction=await container.get(DBTransaction),
            auth=await container.get(adapters.clients.AuthFacade),
            aqua=await container.get(adapters.clients.AquaFacade),
            auth_logger=await container.get(adapters.loggers.AuthFacadeLogger),
            aqua_logger=await container.get(adapters.loggers.AquaFacadeLogger),
        )

    if not isinstance(result, ports.clients.aqua.ReadDayOutput):
        return result

    records = tuple(
        OutputData.RecordData(
            record_id=record.record_id,
            drunk_water_milliliters=record.drunk_water_milliliters,
            recording_time=record.recording_time,
        )
        for record in result.records
    )

    target = result.target_water_balance_milliliters
    return OutputData(
        user_id=result.user_id,
        records=records,
        target_water_balance_milliliters=target,
        date_=result.date_,
        water_balance_milliliters=result.water_balance_milliliters,
        result_code=result.result_code,
        real_result_code=result.real_result_code,
        is_result_pinned=result.is_result_pinned,
    )
