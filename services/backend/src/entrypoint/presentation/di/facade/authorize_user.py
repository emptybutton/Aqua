from dataclasses import dataclass
from datetime import datetime
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application.cases import authorize_user
from entrypoint.application import ports
from entrypoint.infrastructure.adapters import loggers, clients
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    username: str
    session_id: UUID
    session_expiration_date: datetime


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["no_user"]
    | Literal["incorrect_password"]
)


async def perform(name: str, password: str) -> Output:
    async with async_container() as container:
        result = await authorize_user.perform(
            name,
            password,
            transaction=await container.get(DBTransaction, "transactions"),
            auth=await container.get(clients.AuthFacade, "clients"),
            auth_logger=await container.get(
                loggers.AuthFacadeDevLogger, "loggers"
            ),
        )

    if not isinstance(result, ports.clients.auth.AuthorizeUserOutput):
        return result

    return OutputData(
        user_id=result.user_id,
        username=result.username,
        session_id=result.session_id,
        session_expiration_date=result.session_expiration_date,
    )
