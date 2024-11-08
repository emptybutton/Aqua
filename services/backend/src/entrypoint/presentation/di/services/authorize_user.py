from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application import ports
from entrypoint.application.cases import authorize_user
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import sync_container


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    username: str
    session_id: UUID


Output: TypeAlias = (
    OutputData
    | Literal["not_working"]
    | Literal["no_user"]
    | Literal["incorrect_password"]
)


async def perform(session_id: UUID | None, name: str, password: str) -> Output:
    with sync_container() as container:
        result = await authorize_user.perform(
            session_id,
            name,
            password,
            auth=container.get(clients.auth.AuthFacade, "clients"),
            auth_logger=container.get(
                ports.loggers.AuthLogger[clients.auth.AuthFacade], "loggers"
            ),
        )

    if not isinstance(result, ports.clients.auth.AuthorizeUserOutput):
        return result

    return OutputData(
        user_id=result.user_id,
        username=result.username,
        session_id=result.session_id,
    )
