from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypeVar
from uuid import UUID

from auth.application.ports import loggers, repos
from auth.domain import entities
from auth.domain import value_objects as vos
from shared.application.ports.transactions import TransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user: entities.User
    previous_username: entities.PreviousUsername


class Error(Exception): ...


class NoUserError(Error): ...


class NewUsernameTakenError(Error): ...


_UsersT = TypeVar("_UsersT", bound=repos.Users)
_PreviousUsernamesT = TypeVar(
    "_PreviousUsernamesT",
    bound=repos.PreviousUsernames,
)


async def perform(
    user_id: UUID,
    new_username_text: str,
    *,
    users: _UsersT,
    previous_usernames: _PreviousUsernamesT,
    user_transaction_for: TransactionFactory[_UsersT],
    previous_username_transaction_for: TransactionFactory[_PreviousUsernamesT],
    logger: loggers.Logger,
) -> Output:
    new_username = vos.Username(text=new_username_text)

    user_transaction = user_transaction_for(users)
    previous_username_transaction = previous_username_transaction_for(
        previous_usernames,
    )

    async with user_transaction, previous_username_transaction:
        user = await users.find_with_id(user_id)

        if not user:
            raise NoUserError

        found_previous_username = await previous_usernames.find_with_username(
            new_username,
        )

        if (
            found_previous_username
            and found_previous_username.user_id != user.id
        ):
            raise NewUsernameTakenError

        previous_username = user.change_name(
            new_username=new_username,
            current_time=datetime.now(UTC),
        )

        await users.update(user)
        await previous_usernames.add(previous_username)

        await logger.log_renaming(
            user=user,
            previous_username=previous_username,
        )

        return Output(user=user, previous_username=previous_username)
