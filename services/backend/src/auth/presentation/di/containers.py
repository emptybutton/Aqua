from dishka import make_async_container

from auth.presentation.di.providers import (
    GatewayProvider,
    LoggerProvider,
    MepperProvider,
    RepoProvider,
    SqlalchemyProvider,
    TransactionProvider,
    ViewProvider,
)


async_container = make_async_container(
    SqlalchemyProvider(),
    RepoProvider(),
    MepperProvider(),
    LoggerProvider(),
    ViewProvider(),
    GatewayProvider(),
    TransactionProvider(),
)
