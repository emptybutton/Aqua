from datetime import datetime, date
from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application import ports
from entrypoint.application.cases import write_water
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class RecordData:
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


@dataclass(kw_only=True, frozen=True)
class OtherData:
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    date_: date
    previous_records: tuple[RecordData, ...]
    new_record: RecordData


@dataclass(kw_only=True, frozen=True)
class OutputData:
    session_id: UUID
    user_id: UUID
    other: OtherData | Literal["error"] | Literal["incorrect_water_amount"]


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["not_authenticated"]
)


async def perform(
    session_id: UUID,
    milliliters: int | None,
) -> Output:
    async with async_container() as container:
        result = await write_water.perform(
            session_id,
            milliliters,
            transaction=await container.get(DBTransaction),
            auth=await container.get(clients.AuthFacade, "clients"),
            aqua=await container.get(clients.AquaFacade, "clients"),
            auth_logger=await container.get(
                ports.loggers.AuthLogger[clients.AuthFacade], "loggers"
            ),
            aqua_logger=await container.get(
                ports.loggers.AquaLogger[clients.AquaFacade], "loggers"
            ),
        )

    if not isinstance(result, write_water.OutputData):
        return result

    if isinstance(result.aqua_result, ports.clients.aqua.WriteWaterOutput):
        target = result.aqua_result.target_water_balance_milliliters
        water_balance = result.aqua_result.water_balance_milliliters
        previous_records = tuple(map(
            _record_data_of,
            result.aqua_result.previous_records,
        ))
        other = OtherData(
            target_water_balance_milliliters=target,
            water_balance_milliliters=water_balance,
            result_code=result.aqua_result.result_code,
            real_result_code=result.aqua_result.real_result_code,
            is_result_pinned=result.aqua_result.is_result_pinned,
            date_=result.aqua_result.date_,
            new_record=_record_data_of(result.aqua_result.new_record),
            previous_records=previous_records,
        )

    return OutputData(
        session_id=result.auth_result.session_id,
        user_id=result.auth_result.user_id,
        other=other,
    )


def _record_data_of(
    data: ports.clients.aqua.WriteWaterOutput.RecordData
) -> RecordData:
    return RecordData(
        record_id=data.record_id,
        drunk_water_milliliters=data.drunk_water_milliliters,
        recording_time=data.recording_time,
    )
