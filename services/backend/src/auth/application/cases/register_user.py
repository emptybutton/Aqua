from dataclasses import dataclass
from typing import TypeVar

from auth.domain import entities, value_objects as vos
from auth.application.ports import repos, serializers, loggers
from shared.application.ports.transactions import TransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user: entities.User
    session: entities.Session


class Error(Exception): ...


class UserIsAlreadyRegisteredError(Error): ...


_UsersT = TypeVar("_UsersT", bound=repos.Users)
_SessionsT = TypeVar("_SessionsT", bound=repos.Sessions)


async def perform(
    name_text: str,
    password_text: str,
    *,
    users: _UsersT,
    sessions: _SessionsT,
    user_transaction_for: TransactionFactory[_UsersT],
    session_transaction_for: TransactionFactory[_SessionsT],
    password_serializer: serializers.AsymmetricSerializer[
        vos.Password,
        vos.PasswordHash,
    ],
    logger: loggers.Logger,
) -> Output:
    username = vos.Username(text=name_text)
    password = vos.Password(text=password_text)
    password_hash = password_serializer.serialized(password)

    async with user_transaction_for(users):
        if await users.contains_with_name(username):
            raise UserIsAlreadyRegisteredError

        user, session = entities.User.register(username, password_hash)
        await users.add(user)

        async with session_transaction_for(sessions):
            await sessions.add(session)
            await logger.log_registration(user=user, session=session)

            return Output(user=user, session=session)
