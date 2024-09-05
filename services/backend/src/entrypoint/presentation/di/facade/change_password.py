from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application import ports
from entrypoint.application.cases import change_password
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


@dataclass(kw_only=True, frozen=True)
class OkData:
    username: str


Data: TypeAlias = OkData | Literal["error"] | Literal["week_password"]


@dataclass(kw_only=True, frozen=True)
class OutputData:
    session_id: UUID
    user_id: UUID
    data: Data


Output: TypeAlias = OutputData | Literal["error"] | Literal["not_authenticated"]


async def perform(session_id: UUID, new_password: str) -> Output:
    async with async_container() as container:
        result = await change_password.perform(
            session_id,
            new_password,
            transaction=await container.get(DBTransaction, "transactions"),
            auth=await container.get(clients.auth.AuthFacade, "clients"),
            auth_logger=await container.get(
                ports.loggers.AuthLogger[clients.auth.AuthFacade], "loggers"
            ),
        )

    if not isinstance(result, change_password.OutputData):
        return result

    data: Data

    if isinstance(
        result.changing_output, ports.clients.auth.ChangePasswordOutput
    ):
        data = OkData(username=result.changing_output.username)
    else:
        data = result.changing_output

    return OutputData(
        user_id=result.authentication_output.user_id,
        session_id=result.authentication_output.session_id,
        data=data,
    )
