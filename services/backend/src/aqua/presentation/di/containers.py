from dishka import make_async_container

from aqua.presentation.di import providers as aqua_provieers
from shared.presentation.di import providers as shared_providers


adapter_container = make_async_container(
    shared_providers.PeripheryProvider(),
    shared_providers.TransactionProvider(),
    aqua_provieers.RepoProvider(),
    aqua_provieers.LoggerProvider(),
)
