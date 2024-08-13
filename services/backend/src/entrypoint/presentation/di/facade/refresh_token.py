from dataclasses import dataclass
from datetime import datetime
from typing import Literal, TypeAlias

from entrypoint.application.cases import refresh_token as case
from entrypoint.application import ports
from entrypoint.infrastructure import adapters
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    jwt: str


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["invalid_jwt"]
    | Literal["not_utc_refresh_token_expiration_date"]
    | Literal["expired_refresh_token"]
)


async def perform(
    jwt: str,
    refresh_token: str,
    refresh_token_expiration_date: datetime,
) -> Output:
    async with async_container() as container:
        result = await case.perform(
            jwt,
            refresh_token,
            refresh_token_expiration_date,
            transaction=await container.get(DBTransaction),
            auth=await container.get(adapters.clients.AuthFacade),
            auth_logger=await container.get(adapters.loggers.AuthFacadeLogger),
        )

    if not isinstance(result, ports.clients.auth.RefreshTokenOutput):
        return result

    return OutputData(jwt=result.jwt)
