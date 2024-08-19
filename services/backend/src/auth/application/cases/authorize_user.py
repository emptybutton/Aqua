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


class NoUserError(Error): ...


class IncorrectPasswordError(Error): ...


_UsersT = TypeVar("_UsersT", bound=repos.Users)
_SessionsT = TypeVar("_SessionsT", bound=repos.Sessions)


async def perform(
    name_text: str,
    password_text: str,
    *,
    users: _UsersT,
    sessions: _SessionsT,
    password_serializer: serializers.AsymmetricSerializer[
        vos.Password,
        vos.PasswordHash,
    ],
    user_transaction_for: TransactionFactory[_UsersT],
    session_transaction_for: TransactionFactory[_SessionsT],
    logger: loggers.Logger,
) -> Output:
    try:
        username = vos.Username(text=name_text)
    except vos.Username.Error as error:
        raise NoUserError from error

    try:
        password = vos.Password(text=password_text)
    except vos.Password.Error as error:
        raise IncorrectPasswordError from error

    password_hash = password_serializer.serialized(password)

    async with user_transaction_for(users):
        user = await users.find_with_name(username)

        if user is None:
            raise NoUserError

        try:
            user.authorize(password_hash=password_hash)
        except entities.User.IncorrectPasswordHashForAuthorizationError as err:
            raise IncorrectPasswordError from err

        async with session_transaction_for(sessions):
            session = entities.Session.for_(user)
            await sessions.add(session)
            await logger.log_login(user=user, session=session)

            return Output(user=user, session=session)
