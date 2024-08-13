from dishka import make_async_container, make_container

from auth.presentation.di import providers as auth_providers
from shared.presentation.di import providers as shared_providers


async_container = make_async_container(
    shared_providers.PeripheryProvider(),
    shared_providers.TransactionProvider(),
    auth_providers.RepoProvider(),
    auth_providers.GeneratorProvider(),
    auth_providers.SerializerProvider(),
)

sync_container = make_container(
    auth_providers.GeneratorProvider(),
    auth_providers.SerializerProvider(),
)
