from auth.presentation.di import containers


async def perform() -> None:
    containers.sync_container.close()
    await containers.async_container.close()
