from datetime import datetime
from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application.cases import write_water
from entrypoint.infrastructure.adapters import loggers, clients
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_jwt"]
    | Literal["no_user"]
    | Literal["incorrect_water_amount"]
)


async def perform(
    jwt: str,
    milliliters: int | None,
) -> Output:
    async with async_container() as container:
        result = await write_water.perform(
            jwt,
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

    target = result.target_water_balance_milliliters
    return OutputData(
        user_id=result.user_id,
        record_id=result.record_id,
        drunk_water_milliliters=result.drunk_water_milliliters,
        recording_time=result.recording_time,
        target_water_balance_milliliters=target,
        water_balance_milliliters=result.water_balance_milliliters,
        result_code=result.result_code,
        real_result_code=result.real_result_code,
        is_result_pinned=result.is_result_pinned,
    )
