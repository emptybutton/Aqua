from dataclasses import dataclass
from typing import Callable, TypeVar

from src.auth.domain import entities, value_objects
from src.auth.application import errors
from src.auth.application.ports import repos, serializers
from src.auth.application.ports.places import Place
from src.shared.application.ports import uows


_UsersT = TypeVar("_UsersT", bound=repos.Users)


@dataclass(frozen=True)
class OutputDTO:
    user: entities.User
    refresh_token: value_objects.RefreshToken
    serialized_access_token: str


async def register_user(  # noqa: PLR0913
    name_text: str,
    password_text: str,
    refresh_token_place: Place[value_objects.RefreshToken],
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
) -> OutputDTO:
    username = value_objects.Username(name_text)

    password = value_objects.Password(password_text)
    password_hash = password_serializer.serialized(password)

    if await users.has_with_name(username):
        raise errors.UserIsAlreadyRegistered()

    user = entities.User(username, password_hash)

    async with uow_for(users) as uow:
        uow.register_new(user)
        await users.add(user)

    refresh_token = value_objects.RefreshToken(generate_refresh_token_text())
    refresh_token_place.set(refresh_token)

    access_token = value_objects.AccessToken(user.id, user.name)
    serialized_access_token = access_token_serializer.serialized(access_token)

    return OutputDTO(user, refresh_token, serialized_access_token)
