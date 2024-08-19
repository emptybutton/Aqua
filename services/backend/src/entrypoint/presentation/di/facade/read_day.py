from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application.cases import read_day
from entrypoint.infrastructure.adapters import loggers, clients
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
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    records: tuple[RecordData, ...]


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    session_id: UUID
    other: OtherData | None


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["not_authenticated"]
)


async def perform(session_id: UUID, date_: date) -> Output:
    async with async_container() as container:
        result = await read_day.perform(
            session_id,
            date_,
            transaction=await container.get(DBTransaction),
            auth=await container.get(clients.AuthFacade, "clients"),
            aqua=await container.get(clients.AquaFacade, "clients"),
            auth_logger=await container.get(
                loggers.AuthFacadeDevLogger, "loggers"
            ),
            aqua_logger=await container.get(
                loggers.AquaFacadeDevLogger, "loggers"
            ),
        )

    if not isinstance(result, read_day.OutputData):
        return result

    other = None

    if result.aqua_result is not None:
        records = tuple(
            RecordData(
                record_id=record.record_id,
                drunk_water_milliliters=record.drunk_water_milliliters,
                recording_time=record.recording_time,
            )
            for record in result.aqua_result.records
        )

        target = result.aqua_result.target_water_balance_milliliters
        water_balance = result.aqua_result.water_balance_milliliters
        other = OtherData(
            target_water_balance_milliliters=target,
            date_=result.aqua_result.date_,
            water_balance_milliliters=water_balance,
            result_code=result.aqua_result.result_code,
            real_result_code=result.aqua_result.real_result_code,
            is_result_pinned=result.aqua_result.is_result_pinned,
            records=records,
        )


    return OutputData(
        user_id=result.auth_result.user_id,
        session_id=result.auth_result.session_id,
        other=other,
    )
