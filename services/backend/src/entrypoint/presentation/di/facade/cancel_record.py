from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application import ports
from entrypoint.application.cases import cancel_record
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class RecordData:
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


@dataclass(kw_only=True, frozen=True)
class OkData:
    target_water_balance_milliliters: int
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    day_records: tuple[RecordData, ...]
    cancelled_record: RecordData


Data: TypeAlias = OkData | Literal["error"] | Literal["no_record"]


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    session_id: UUID
    data: Data


Output: TypeAlias = (
    OutputData | Literal["error"] | Literal["not_authenticated"]
)


async def perform(session_id: UUID, record_id: UUID) -> Output:
    async with async_container() as container:
        result = await cancel_record.perform(
            session_id,
            record_id,
            transaction=await container.get(DBTransaction, "transactions"),
            auth=await container.get(clients.auth.AuthFacade, "clients"),
            aqua=await container.get(clients.aqua.AquaFacade, "clients"),
            auth_logger=await container.get(
                ports.loggers.AuthLogger[clients.auth.AuthFacade], "loggers"
            ),
            aqua_logger=await container.get(
                ports.loggers.AquaLogger[clients.aqua.AquaFacade], "loggers"
            ),
        )

    if not isinstance(result, cancel_record.OutputData):
        return result

    data: Data

    if isinstance(result.aqua_output, ports.clients.aqua.CancelRecordOutput):
        day_records = tuple(
            map(_record_data_of, result.aqua_output.day_records)
        )
        cancelled_record = _record_data_of(result.aqua_output.cancelled_record)
        target = result.aqua_output.target_water_balance_milliliters
        water_balance = result.aqua_output.water_balance_milliliters
        data = OkData(
            target_water_balance_milliliters=target,
            date_=result.aqua_output.date_,
            water_balance_milliliters=water_balance,
            result_code=result.aqua_output.result_code,
            real_result_code=result.aqua_output.real_result_code,
            is_result_pinned=result.aqua_output.is_result_pinned,
            day_records=day_records,
            cancelled_record=cancelled_record,
        )
    else:
        data = result.aqua_output

    return OutputData(
        user_id=result.auth_output.user_id,
        session_id=result.auth_output.session_id,
        data=data,
    )


def _record_data_of(
    other_record_data: ports.clients.aqua.CancelRecordOutput.RecordData
) -> RecordData:
    return RecordData(
        record_id=other_record_data.record_id,
        drunk_water_milliliters=other_record_data.drunk_water_milliliters,
        recording_time=other_record_data.recording_time,
    )
