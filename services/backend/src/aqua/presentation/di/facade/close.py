from aqua.infrastructure.periphery.storages.mongo.clients import client
from aqua.presentation.di import containers


async def perform() -> None:
    await containers.adapter_container.close()
    await client.close()
