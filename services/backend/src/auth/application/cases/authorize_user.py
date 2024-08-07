from dataclasses import dataclass
from typing import Callable

from auth.domain import entities, value_objects as vos
from auth.application.ports import repos, serializers


@dataclass(kw_only=True, frozen=True)
class Output:
    user: entities.User
    refresh_token: vos.RefreshToken
    serialized_access_token: str


class Error(Exception): ...


class NoUserError(Error): ...


class IncorrectPasswordError(Error): ...


async def perform(  # noqa: PLR0913
    name_text: str,
    password_text: str,
    *,
    users: repos.Users,
    password_serializer: serializers.AsymmetricSerializer[
        vos.Password,
        vos.PasswordHash,
    ],
    access_token_serializer: serializers.SecureSymmetricSerializer[
        vos.AccessToken,
        str,
    ],
    generate_refresh_token_text: Callable[[], str],
) -> Output:
    try:
        username = vos.Username(text=name_text)
    except vos.Username.Error as error:
        raise NoUserError from error

    user = await users.find_with_name(username)

    if user is None:
        raise NoUserError

    try:
        password = vos.Password(text=password_text)
    except vos.Password.Error as error:
        raise IncorrectPasswordError from error

    password_hash = password_serializer.serialized(password)

    try:
        user.authorize(password_hash=password_hash)
    except entities.User.IncorrectPasswordHashForAuthorizationError as error:
        raise IncorrectPasswordError from error

    refresh_token = vos.RefreshToken(text=generate_refresh_token_text())

    access_token = vos.AccessToken(user_id=user.id)
    serialized_access_token = access_token_serializer.serialized(access_token)

    return Output(
        user=user,
        refresh_token=refresh_token,
        serialized_access_token=serialized_access_token,
    )
