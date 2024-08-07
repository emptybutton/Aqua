from typing import Annotated

from dishka import Provider, provide, Scope, FromComponent
from sqlalchemy.ext.asyncio import AsyncSession

from auth.infrastructure import adapters
from shared.infrastructure.periphery.envs import Env


class RepoProvider(Provider):
    component = "repos"

    @provide(scope=Scope.REQUEST)
    def get_a(
        self,
        session: Annotated[AsyncSession, FromComponent("periphery")],
    ) -> adapters.repos.DBUsers:
        return adapters.repos.DBUsers(session)


class GeneratorProvider(Provider):
    component = "generators"

    @provide(scope=Scope.APP)
    def get_a(
        self,
    ) -> adapters.generators.GenerateByTokenHex:
        return adapters.generators.GenerateByTokenHex()


class SerializerProvider(Provider):
    component = "serializers"

    @provide(scope=Scope.APP)
    def get_a(
        self,
    ) -> adapters.serializers.AccessTokenSerializer:
        return adapters.serializers.AccessTokenSerializer(Env.jwt_secret)

    @provide(scope=Scope.APP)
    def get_b(self) -> adapters.serializers.PasswordSerializer:
        return adapters.serializers.PasswordSerializer()
