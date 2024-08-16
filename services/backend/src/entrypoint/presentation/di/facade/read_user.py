from dataclasses import dataclass
from datetime import datetime, date
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application.cases import read_user
from entrypoint.infrastructure.adapters import loggers, clients
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    @dataclass(kw_only=True, frozen=True)
    class AuthPart:
        username: str

    @dataclass(kw_only=True, frozen=True)
    class AquaPart:
        glass_milliliters: int
        weight_kilograms: int | None
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

    user_id: UUID
    auth_part: AuthPart | None = None
    aqua_part: AquaPart | None = None


Output: TypeAlias = (
    OutputData
    | None
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_jwt"]
)


async def perform(jwt: str) -> Output:
    async with async_container() as container:
        result = await read_user.perform(
            jwt,
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

    if not isinstance(result, read_user.OutputData):
        return result

    aqua_part = None
    auth_part = None

    if result.aqua_part is not None:
        target = result.aqua_part.target_water_balance_milliliters
        records = tuple(
            OutputData.AquaPart.RecordData(
                record_id=record.record_id,
                drunk_water_milliliters=record.drunk_water_milliliters,
                recording_time=record.recording_time,
            )
            for record in result.aqua_part.records
        )

        aqua_part = OutputData.AquaPart(
            records=records,
            glass_milliliters=result.aqua_part.glass_milliliters,
            weight_kilograms=result.aqua_part.weight_kilograms,
            target_water_balance_milliliters=target,
            date_=result.aqua_part.date_,
            water_balance_milliliters=result.aqua_part.water_balance_milliliters,
            result_code=result.aqua_part.result_code,
            real_result_code=result.aqua_part.real_result_code,
            is_result_pinned=result.aqua_part.is_result_pinned,
        )

    if result.auth_part is not None:
        auth_part = OutputData.AuthPart(username=result.auth_part.username)

    return OutputData(
        user_id=result.user_id,
        aqua_part=aqua_part,
        auth_part=auth_part,
    )
