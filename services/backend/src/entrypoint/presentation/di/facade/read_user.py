from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application.cases import read_user
from entrypoint.application import ports
from entrypoint.infrastructure import adapters
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    username: str
    glass_milliliters: int
    target_water_balance_milliliters: int
    weight_kilograms: int | None


Output: TypeAlias = (
    OutputData
    | None
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_access_token"]
)


async def perform(jwt: str) -> Output:
    async with async_container() as container:
        result = await read_user.perform(
            jwt,
            transaction=await container.get(DBTransaction),
            auth=await container.get(adapters.clients.AuthFacade),
            aqua=await container.get(adapters.clients.AquaFacade),
            auth_logger=await container.get(adapters.loggers.AuthFacadeLogger),
            aqua_logger=await container.get(adapters.loggers.AquaFacadeLogger),
        )

    if not isinstance(result, read_user.OutputData):
        return result

    return OutputData(
        user_id=result.user_id,
        username=result.username,
        glass_milliliters=result.glass_milliliters,
        target_water_balance_milliliters=result.target_water_balance_milliliters,
        weight_kilograms=result.weight_kilograms,
    )
