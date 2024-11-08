from typing import Literal, TypeAlias

from entrypoint.application import ports
from entrypoint.application.cases import user_exists
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import sync_container


Output: TypeAlias = bool | Literal["error"]


async def perform(username: str) -> Output:
    with sync_container() as container:
        return await user_exists.perform(
            username,
            auth=container.get(clients.auth.AuthFacade, "clients"),
            auth_logger=container.get(
                ports.loggers.AuthLogger[clients.auth.AuthFacade], "loggers"
            ),
        )
