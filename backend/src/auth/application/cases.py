from typing import Callable, TypeVar, Optional

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
    refresh_token_container: repos.Container[value_objects.RefreshToken],
    *,
    users: _UsersT,
    uow_for: Callable[[_UsersT], uows.UoW[entities.User]],
    access_token_serializer: serializers.SymmetricSerializer[
        value_objects.AccessToken,
        str,
    ],
    password_serializer: serializers.AsymmetricSerializer[
        value_objects.Password,
        value_objects.PasswordHash,
    ],
    generate_refresh_token_text: Callable[[], str],
) -> dtos.Registration:
    username = value_objects.Username(name_text)

    password = value_objects.Password(password_text)
    password_hash = password_serializer.serialized(password)

    if users.has_with_name(username):
        raise errors.UserIsAlreadyRegistered()

    user = entities.User(None, username, password_hash)

    async with uow_for(users) as uow:
        uow.register_new(user)
        users.add(user)

    refresh_token = value_objects.RefreshToken(generate_refresh_token_text())
    refresh_token_container.set(refresh_token)

    access_token = value_objects.AccessToken(user.id, user.name)
    serialized_access_token = access_token_serializer.serialized(access_token)

    return dtos.Registration(user, refresh_token, serialized_access_token)


def authenticate_user(
    serialized_access_token: str,
    refresh_token_container: _RefreshTokenContainerT,
    *,
    access_token_serializer: serializers.SymmetricSerializer[
        value_objects.AccessToken,
        str,
    ],
    generate_refresh_token_text: Callable[[], str],
) -> Optional[dtos.Authentication]:
    access_token = access_token_serializer.deserialized(serialized_access_token)

    if access_token is None:
        raise errors.UserIsNotAuthenticated()

    if not access_token.is_expired:
        return None

    refresh_token = refresh_token_container.get()

    if refresh_token is None or refresh_token.is_expired:
        raise errors.UserIsNotAuthenticated()

    new_access_token = value_objects.AccessToken(
        access_token.user_id,
        access_token.username,
    )

    new_refresh_token_text = generate_refresh_token_text()
    new_refresh_token = value_objects.RefreshToken(new_refresh_token_text)

    refresh_token_container.set(new_refresh_token)

    return dtos.Authentication(
        new_refresh_token,
        access_token_serializer.serialized(new_access_token),
    )
