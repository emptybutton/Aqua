from dishka import Provider, Scope, provide

from entrypoint.application import ports
from entrypoint.infrastructure import adapters
from entrypoint.infrastructure.periphery import envs


class LogerProvider(Provider):
    component = "loggers"

    @provide(scope=Scope.APP)
    def get_aqua_logger(
        self,
    ) -> ports.loggers.AquaLogger[adapters.clients.aqua.AquaFacade]:
        if envs.is_dev:
            return adapters.loggers.AquaFacadeDevLogger()

        return adapters.loggers.AquaFacadeProdLogger()

    @provide(scope=Scope.APP)
    def get_auth_logger(
        self,
    ) -> ports.loggers.AuthLogger[adapters.clients.auth.AuthFacade]:
        if envs.is_dev:
            return adapters.loggers.AuthFacadeDevLogger()

        return adapters.loggers.AuthFacadeProdLogger()


class ClientProvider(Provider):
    component = "clients"

    @provide(scope=Scope.REQUEST)
    def get_aqua(self) -> adapters.clients.aqua.AquaFacade:
        return adapters.clients.aqua.AquaFacade()

    @provide(scope=Scope.REQUEST)
    def get_auth(self) -> adapters.clients.auth.AuthFacade:
        return adapters.clients.auth.AuthFacade()
