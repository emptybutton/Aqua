from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application import ports
from entrypoint.application.cases import read_user
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import sync_container


@dataclass(kw_only=True, frozen=True)
class FirstPart:
    username: str


@dataclass(kw_only=True, frozen=True)
class RecordData:
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


@dataclass(kw_only=True, frozen=True)
class SecondPart:
    glass_milliliters: int
    weight_kilograms: int | None
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
    first_part: FirstPart | None = None
    second_part: SecondPart | None = None


Output: TypeAlias = (
    OutputData | Literal["not_working"] | Literal["not_authenticated"]
)


async def perform(session_id: UUID) -> Output:
    with sync_container() as container:
        result = await read_user.perform(
            session_id,
            auth=await container.get(clients.auth.AuthFacade, "clients"),
            aqua=await container.get(clients.aqua.AquaFacade, "clients"),
            auth_logger=await container.get(
                ports.loggers.AuthLogger[clients.auth.AuthFacade], "loggers"
            ),
            aqua_logger=await container.get(
                ports.loggers.AquaLogger[clients.aqua.AquaFacade], "loggers"
            ),
        )

    if not isinstance(result, read_user.OutputData):
        return result

    first_part = None
    second_part = None

    if result.read_auth_user_result is not None:
        first_part = FirstPart(username=result.read_auth_user_result.username)

    if result.read_aqua_user_result is not None:
        records = tuple(
            RecordData(
                record_id=record.record_id,
                drunk_water_milliliters=record.drunk_water_milliliters,
                recording_time=record.recording_time,
            )
            for record in result.read_aqua_user_result.records
        )

        target = result.read_aqua_user_result.target_water_balance_milliliters
        water_balance = result.read_aqua_user_result.water_balance_milliliters
        second_part = SecondPart(
            glass_milliliters=result.read_aqua_user_result.glass_milliliters,
            weight_kilograms=result.read_aqua_user_result.weight_kilograms,
            target_water_balance_milliliters=target,
            date_=result.read_aqua_user_result.date_,
            water_balance_milliliters=water_balance,
            result_code=result.read_aqua_user_result.result_code,
            real_result_code=result.read_aqua_user_result.real_result_code,
            is_result_pinned=result.read_aqua_user_result.is_result_pinned,
            records=records,
        )

    return OutputData(
        user_id=result.authenticate_user_result.user_id,
        session_id=result.authenticate_user_result.session_id,
        first_part=first_part,
        second_part=second_part,
    )
