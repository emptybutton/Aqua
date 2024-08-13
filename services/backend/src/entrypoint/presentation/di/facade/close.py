from entrypoint.application.cases import close
from entrypoint.infrastructure import adapters
from entrypoint.presentation.di import containers


async def perform() -> None:
    async with containers.async_container() as container:
        await close.perform(
            auth=await container.get(adapters.clients.AuthFacade),
            aqua=await container.get(adapters.clients.AquaFacade),
        )

    await containers.async_container.close()
    containers.sync_container.close()
