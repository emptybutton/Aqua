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


class UserIsAlreadyRegisteredError(Error): ...


_UsersT = TypeVar("_UsersT", bound=repos.Users)
_SessionsT = TypeVar("_SessionsT", bound=repos.Sessions)


async def perform(
    session_id: UUID | None,
    name_text: str,
    password_text: str,
    *,
    users: _UsersT,
    sessions: _SessionsT,
    previous_usernames: repos.PreviousUsernames,
    user_transaction_for: TransactionFactory[_UsersT],
    session_transaction_for: TransactionFactory[_SessionsT],
    password_serializer: serializers.AsymmetricSerializer[
        vos.Password, vos.PasswordHash
    ],
    logger: loggers.Logger,
) -> Output:
    current_time = vos.Time(datetime_=datetime.now(UTC))

    username = vos.Username(text=name_text)
    password = vos.Password(text=password_text)
    password_hash = password_serializer.serialized(password)

    if await previous_usernames.contains_with_username(username):
        raise UserIsAlreadyRegisteredError

    async with user_transaction_for(users), session_transaction_for(sessions):
        current_session = None

        if session_id is not None:
            current_session = await sessions.find_with_id(session_id)

        if await users.contains_with_name(username):
            raise UserIsAlreadyRegisteredError

        result = entities.User.register(
            username,
            password_hash,
            current_time=current_time,
            current_session=current_session,
        )

        await users.add(result.user)

        if result.new_session is not None:
            await sessions.add(result.new_session)

        if result.extended_session is not None:
            await logger.log_session_extension(result.extended_session)
            await sessions.update(result.extended_session)

        if result.replaced_session is not None:
            await logger.log_replaced_session(result.replaced_session)
            await sessions.update(result.replaced_session)

        await logger.log_registration(
            user=result.user, session=result.current_session
        )

        return Output(user=result.user, session=result.current_session)
