from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypeVar
from uuid import UUID

from auth.application.ports import loggers, repos, serializers
from auth.domain import entities
from auth.domain import value_objects as vos
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
    session_id: UUID | None,
    name_text: str,
    password_text: str,
    *,
    users: _UsersT,
    sessions: _SessionsT,
    password_serializer: serializers.AsymmetricSerializer[
        vos.Password, vos.PasswordHash
    ],
    user_transaction_for: TransactionFactory[_UsersT],
    session_transaction_for: TransactionFactory[_SessionsT],
    logger: loggers.Logger,
) -> Output:
    current_time = vos.Time(datetime_=datetime.now(UTC))

    try:
        username = vos.Username(text=name_text)
    except vos.Username.Error as error:
        raise NoUserError from error

    try:
        password = vos.Password(text=password_text)
    except vos.Password.Error as error:
        raise IncorrectPasswordError from error

    password_hash = password_serializer.serialized(password)

    async with user_transaction_for(users), session_transaction_for(sessions):
        user = await users.find_with_name(username)

        if user is None:
            raise NoUserError

        if session_id is not None:
            current_session = await sessions.find_with_id(session_id)
        else:
            current_session = None

        try:
            result = user.authorize(
                password_hash=password_hash,
                current_time=current_time,
                current_session=current_session,
            )
        except entities.User.IncorrectPasswordHashForAuthorizationError as err:
            raise IncorrectPasswordError from err

        if result.new_session is not None:
            await sessions.add(result.new_session)

        if result.extended_session is not None:
            await logger.log_session_extension(result.extended_session)
            await sessions.update(result.extended_session)

        await logger.log_login(user=user, session=result.current_session)

        return Output(user=user, session=result.current_session)
