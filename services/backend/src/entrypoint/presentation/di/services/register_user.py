from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application import ports
from entrypoint.application.cases import register_user
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import sync_container


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
    | Literal["user_is_already_registered"]
    | Literal["empty_username"]
    | Literal["week_password"]
)


async def perform(  # noqa: PLR0917
    session_id: UUID | None,
    name: str,
    password: str,
    target_water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
) -> Output:
    with sync_container() as container:
        result = await register_user.perform(
            session_id,
            name,
            password,
            target_water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            aqua=container.get(clients.aqua.AquaFacade, "clients"),
            auth=container.get(clients.auth.AuthFacade, "clients"),
            aqua_logger=container.get(
                ports.loggers.AquaLogger[clients.aqua.AquaFacade], "loggers"
            ),
            auth_logger=container.get(
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
