from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application import ports
from entrypoint.application.cases import register_user
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    session_id: UUID
    user_id: UUID
    username: str
    target_water_balance_milliliters: int
    glass_milliliters: int
    weight_kilograms: int | None


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["incorrect_water_amount"]
    | Literal["incorrect_weight_amount"]
    | Literal["no_weight_for_water_balance"]
    | Literal["extreme_weight_for_water_balance"]
    | Literal["empty_username"]
    | Literal["week_password"]
)


async def perform(
    name: str,
    password: str,
    target_water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
) -> Output:
    async with async_container() as container:
        result = await register_user.perform(
            name,
            password,
            target_water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            transaction=await container.get(DBTransaction, "transactions"),
            aqua=await container.get(clients.aqua.AquaFacade, "clients"),
            auth=await container.get(clients.auth.AuthFacade, "clients"),
            aqua_logger=await container.get(
                ports.loggers.AquaLogger[clients.aqua.AquaFacade], "loggers"
            ),
            auth_logger=await container.get(
                ports.loggers.AuthLogger[clients.auth.AuthFacade], "loggers"
            ),
        )

    if not isinstance(result, register_user.OutputData):
        return result

    target = result.aqua_result.target_water_balance_milliliters
    return OutputData(
        user_id=result.auth_result.user_id,
        username=result.auth_result.username,
        session_id=result.auth_result.session_id,
        target_water_balance_milliliters=target,
        glass_milliliters=result.aqua_result.glass_milliliters,
        weight_kilograms=result.aqua_result.weight_kilograms,
    )
