from dataclasses import dataclass
from datetime import date
from typing import Literal, TypeAlias

from entrypoint.application.cases import read_day
from entrypoint.application import ports
from entrypoint.infrastructure import adapters
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    target_water_balance: int
    real_water_balance: int
    result_code: int


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["expired_access_token"]
    | Literal["no_user"]
)


async def perform(jwt: str, date_: date) -> Output:
    async with async_container() as container:
        result = await read_day.perform(
            jwt,
            date_,
            transaction=await container.get(DBTransaction),
            auth=await container.get(adapters.clients.AuthFacade),
            aqua=await container.get(adapters.clients.AquaFacade),
            auth_logger=await container.get(adapters.loggers.AuthFacadeLogger),
            aqua_logger=await container.get(adapters.loggers.AquaFacadeLogger),
        )

    if not isinstance(result, ports.clients.aqua.ReadDayOutput):
        return result

    return OutputData(
        target_water_balance=result.target_water_balance,
        real_water_balance=result.real_water_balance,
        result_code=result.result_code,
    )
