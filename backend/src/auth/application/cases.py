from typing import Callable, TypeVar

from src.auth.domain import entities, value_objects
from src.auth.application import errors, dtos
from src.auth.application.ports import repos, serializers
from src.shared.application.ports import uows


_UsersT = TypeVar("_UsersT", bound=repos.Users)
_RefreshTokenContainerT = TypeVar(
    "_RefreshTokenContainerT",
    bound=repos.Container[value_objects.RefreshToken],
)


async def register_user(  # noqa: PLR0913
    name_text: str,
    password_text: str,
    *,
    users: _UsersT,
    refresh_token_container: _RefreshTokenContainerT,
    user_uow_for: Callable[[_UsersT], uows.UoW[entities.User]],
    refresh_token_uow_for: Callable[
        [_RefreshTokenContainerT],
        uows.UoW[value_objects.RefreshToken]
    ],
    access_token_serializer: serializers.Serializer[
        value_objects.AccessToken,
        str,
    ],
) -> dtos.Registration:
    username = value_objects.Username(name_text)

    password = value_objects.Password(password_text)
    password_hash = value_objects.PasswordHash.of(password)

    if users.has_with_name(username):
        raise errors.UserIsAlreadyRegistered()

    user = entities.User(None, username, password_hash)

    user_uow = user_uow_for(users)
    refresh_token_uow = refresh_token_uow_for(refresh_token_container)

    async with user_uow as user_uow, refresh_token_uow as refresh_token_uow:
        user_uow.register_new(user)
        users.add(user)

        refresh_token = value_objects.RefreshToken()
        refresh_token_uow.register_new(refresh_token)
        refresh_token_container.set(refresh_token)

    access_token = value_objects.AccessToken(user.id, user.name)
    serialized_access_token = access_token_serializer.serialize(access_token)

    return dtos.Registration(user, serialized_access_token, refresh_token.text)


def authenticate_user(
    serialized_access_token: str,
    *,
    refresh_token_container: _RefreshTokenContainerT,
    access_token_serializer: serializers.Serializer[
        value_objects.AccessToken,
        str,
    ],
) -> dtos.Authentication:
    access_token = access_token_serializer.deserialize(serialized_access_token)

    if access_token is None:
        raise errors.UserIsNotAuthenticated()

    if not access_token.is_expired:
        return dtos.Authentication()

    refresh_token = refresh_token_container.get()

    if refresh_token is None:
        raise errors.UserIsNotAuthenticated()

    new_access_token = value_objects.AccessToken(
        access_token.user_id,
        access_token.username,
    )

    return dtos.Authentication(
        access_token_serializer.serialize(new_access_token),
    )
