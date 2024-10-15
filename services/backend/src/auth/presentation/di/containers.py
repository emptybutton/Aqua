from dishka import make_async_container

from auth.presentation.di import providers as auth_providers
from shared.presentation.di import providers as shared_providers


async_container = make_async_container(
    shared_providers.MultilevelPeripheryProvider(),
    shared_providers.ConnectionTransactionProvider(),
    shared_providers.IndexProvider(),
    auth_providers.RepoProvider(),
    auth_providers.MepperProvider(),
    auth_providers.LoggerProvider(),
    auth_providers.ViewProvider(),
    auth_providers.GatewayProvider(),
)
