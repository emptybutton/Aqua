from dishka import make_async_container, make_container

from entrypoint.presentation.di import providers as entrypoint_providers
from shared.presentation.di import providers as shared_providers


async_container = make_async_container(
    shared_providers.TransactionProvider(),
    entrypoint_providers.PeripheryProvider(),
    entrypoint_providers.LogerProvider(),
    entrypoint_providers.ClientProvider(),
)

sync_container = make_container(
    entrypoint_providers.LogerProvider(), entrypoint_providers.ClientProvider()
)
