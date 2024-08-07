from dishka import make_async_container, make_container

from auth.presentation.di import providers as auth_provieers
from shared.presentation.di import providers as shared_providers


async_container = make_async_container(
    shared_providers.PeripheryProvider(),
    shared_providers.TransactionProvider(),
    auth_provieers.RepoProvider(),
    auth_provieers.GeneratorProvider(),
    auth_provieers.SerializerProvider(),
)

sync_container = make_container(
    auth_provieers.GeneratorProvider(),
    auth_provieers.SerializerProvider(),
)
