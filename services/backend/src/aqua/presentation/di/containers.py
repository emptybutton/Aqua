from dishka import make_async_container

from aqua.presentation.di import providers


adapter_container = make_async_container(
    providers.MongoProvider(),
    providers.LoggerProvider(),
    providers.MapperProvider(),
    providers.RepoProvider(),
    providers.TransactionProvider(),
    providers.ViewProvider(),
)
