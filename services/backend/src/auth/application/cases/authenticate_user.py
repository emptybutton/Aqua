from typing import TypeVar

from auth.domain import value_objects as vos
from auth.application import ports


class Error(Exception): ...


class NoAccessTokenError(Error): ...


_UsersT = TypeVar("_UsersT", bound=ports.repos.Users)


async def perform(
    serialized_access_token: str,
    *,
    access_token_serializer: ports.serializers.SecureSymmetricSerializer[
        vos.AccessToken,
        str,
    ],
) -> vos.AccessToken:
    access_token = access_token_serializer.deserialized(serialized_access_token)

    if access_token is None:
        raise NoAccessTokenError

    access_token.authenticate()

    return access_token
