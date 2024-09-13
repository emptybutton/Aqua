from typing import Literal, TypeAlias

from entrypoint.application import ports
from entrypoint.application.cases import user_exists
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransaction


Output: TypeAlias = bool | Literal["error"]


async def perform(username: str) -> Output:
    async with async_container() as container:
        return await user_exists.perform(
            username,
            transaction=await container.get(DBTransaction, "transactions"),
            auth=await container.get(clients.auth.AuthFacade, "clients"),
            auth_logger=await container.get(
                ports.loggers.AuthLogger[clients.auth.AuthFacade], "loggers"
            ),
        )
