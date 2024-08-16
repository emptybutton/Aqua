from entrypoint.application.cases import close
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di import containers


async def perform() -> None:
    async with containers.async_container() as container:
        await close.perform(
            auth=await container.get(clients.AuthFacade, "clients"),
            aqua=await container.get(clients.AquaFacade, "clients"),
        )

    await containers.async_container.close()
    containers.sync_container.close()
