from aqua.presentation.di import containers


async def perform() -> None:
    await containers.adapter_container.close()
