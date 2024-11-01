from aqua.infrastructure.periphery.storages.mongodb.clients import client
from aqua.presentation.di import containers


async def perform() -> None:
    await containers.adapter_container.close()
    await client.close()
