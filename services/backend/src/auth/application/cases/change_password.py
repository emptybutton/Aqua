from dataclasses import dataclass
from typing import TypeVar
from uuid import UUID

from auth.application.ports import loggers, repos, serializers
from auth.domain import entities
from auth.domain import value_objects as vos
from shared.application.ports.transactions import TransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user: entities.User
    other_sessions: tuple[entities.Session, ...]


class Error(Exception): ...


class NoUserError(Error): ...


_UsersT = TypeVar("_UsersT", bound=repos.Users)
_SessionsT = TypeVar("_SessionsT", bound=repos.Sessions)


async def perform(
    user_id: UUID,
    new_password_text: str,
    current_session_id: UUID,
    *,
    users: _UsersT,
    sessions: _SessionsT,
    user_transaction_for: TransactionFactory[_UsersT],
    session_transaction_for: TransactionFactory[_SessionsT],
    logger: loggers.Logger,
    password_serializer: serializers.AsymmetricSerializer[
        vos.Password, vos.PasswordHash
    ],
) -> Output:
    new_password = vos.Password(text=new_password_text)
    new_password_hash = password_serializer.serialized(new_password)

    async with user_transaction_for(users), session_transaction_for(sessions):
        user = await users.find_with_id(user_id)

        if not user:
            raise NoUserError

        found_other_sessions = await sessions.find_other_with_user_id(
            current_session_id=current_session_id,
            user_id=user.id,
        )

        user.change_password(
            new_password_hash=new_password_hash,
            other_sessions=found_other_sessions,
        )

        await users.update(user)
        await sessions.update_all(found_other_sessions)

        await logger.log_password_change(
            user=user,
            other_sessions=found_other_sessions,
        )

        return Output(user=user, other_sessions=found_other_sessions)
