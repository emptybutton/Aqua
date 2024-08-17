from datetime import datetime
from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application import ports
from entrypoint.application.cases import write_water
from entrypoint.infrastructure.adapters import loggers, clients
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OtherData:
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool


@dataclass(kw_only=True, frozen=True)
class OutputData:
    session_id: UUID
    session_expiration_date: datetime
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
                loggers.AuthFacadeLogger, "loggers"
            ),
            aqua_logger=await container.get(
                loggers.AquaFacadeLogger, "loggers"
            ),
        )

    if not isinstance(result, write_water.OutputData):
        return result

    if isinstance(result.aqua_result, ports.clients.aqua.WriteWaterOutput):
        target = result.aqua_result.target_water_balance_milliliters
        water_balance = result.aqua_result.water_balance_milliliters
        other = OtherData(
            record_id=result.aqua_result.record_id,
            drunk_water_milliliters=result.aqua_result.drunk_water_milliliters,
            recording_time=result.aqua_result.recording_time,
            target_water_balance_milliliters=target,
            water_balance_milliliters=water_balance,
            result_code=result.aqua_result.result_code,
            real_result_code=result.aqua_result.real_result_code,
            is_result_pinned=result.aqua_result.is_result_pinned,
        )

    return OutputData(
        session_id=result.auth_result.session_id,
        session_expiration_date=result.auth_result.session_expiration_date,
        user_id=result.auth_result.user_id,
        other=other,
    )
