from dishka import make_async_container

from aqua.presentation.di import providers


adapter_container = make_async_container(
    providers.MultilevelPeripheryProvider(),
    providers.RepoProvider(),
    providers.LoggerProvider(),
)
