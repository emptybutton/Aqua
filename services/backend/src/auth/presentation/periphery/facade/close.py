from auth.presentation.di import containers


async def perform() -> None:
    await containers.async_container.close()
