from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application.cases import write_water
from entrypoint.infrastructure import adapters
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    record_id: UUID
    drunk_water_milliliters: int


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
            auth=await container.get(adapters.clients.AuthFacade),
            aqua=await container.get(adapters.clients.AquaFacade),
            auth_logger=await container.get(adapters.loggers.AuthFacadeLogger),
            aqua_logger=await container.get(adapters.loggers.AquaFacadeLogger),
        )

    if not isinstance(result, write_water.OutputData):
        return result

    return OutputData(
        user_id=result.user_id,
        record_id=result.record_id,
        drunk_water_milliliters=result.drunk_water_milliliters,
    )
