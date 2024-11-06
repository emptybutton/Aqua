from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import sync_container


async def perform() -> None:
    with sync_container() as container:
        auth = container.get(clients.auth.AuthFacade, "clients")
        aqua = container.get(clients.aqua.AquaFacade, "clients")

    await auth.close()
    await aqua.close()

    sync_container.close()
