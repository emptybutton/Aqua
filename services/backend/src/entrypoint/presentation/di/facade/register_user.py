from dataclasses import dataclass
from datetime import datetime
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application.cases import register_user
from entrypoint.infrastructure import adapters
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    username: str
    access_token: str
    refresh_token: str
    refresh_token_expiration_date: datetime
    water_balance_milliliters: int
    glass_milliliters: int


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


async def perform(
    name: str,
    password: str,
    water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
) -> Output:
    async with async_container() as container:
        result = await register_user.perform(
            name,
            password,
            water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            transaction=await container.get(DBTransaction),
            auth=await container.get(adapters.clients.AuthFacade),
            aqua=await container.get(adapters.clients.AquaFacade),
            auth_logger=await container.get(adapters.loggers.AuthFacadeLogger),
            aqua_logger=await container.get(adapters.loggers.AquaFacadeLogger),
        )

    if not isinstance(result, register_user.OutputData):
        return result

    return OutputData(
        user_id=result.user_id,
        username=result.username,
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        refresh_token_expiration_date=result.refresh_token_expiration_date,
        water_balance_milliliters=result.water_balance_milliliters,
        glass_milliliters=result.glass_milliliters,
    )
