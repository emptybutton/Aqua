from dataclasses import dataclass
from typing import TypeVar

from auth.domain import entities, value_objects as vos
from auth.application.ports import repos, serializers, generators
from shared.application.ports.transactions import TransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user: entities.User
    refresh_token: vos.RefreshToken
    serialized_access_token: str


class Error(Exception): ...


class UserIsAlreadyRegisteredError(Error): ...


_UsersT = TypeVar("_UsersT", bound=repos.Users)


async def perform(  # noqa: PLR0913
    name_text: str,
    password_text: str,
    *,
    users: _UsersT,
    transaction_for: TransactionFactory[_UsersT],
    access_token_serializer: serializers.SecureSymmetricSerializer[
        vos.AccessToken,
        str,
    ],
    password_serializer: serializers.AsymmetricSerializer[
        vos.Password,
        vos.PasswordHash,
    ],
    generate_high_entropy_text: generators.GenerateHighEntropyText,
) -> Output:
    username = vos.Username(text=name_text)
    password = vos.Password(text=password_text)
    password_hash = password_serializer.serialized(password)
    refresh_token = vos.RefreshToken(text=generate_high_entropy_text())

    async with transaction_for(users):
        if await users.contains_with_name(username):
            raise UserIsAlreadyRegisteredError

        user = entities.User(name=username, password_hash=password_hash)
        await users.add(user)

        access_token = vos.AccessToken(user_id=user.id)
        serialized_access_token = (
            access_token_serializer.serialized(access_token)
        )

        return Output(
            user=user,
            refresh_token=refresh_token,
            serialized_access_token=serialized_access_token,
        )
