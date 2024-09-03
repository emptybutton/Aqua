from dataclasses import dataclass
from typing import TypeVar
from uuid import UUID

from auth.application.ports import repos
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
) -> Output:
    new_username = vos.Username(text=new_username_text)

    async with user_transaction_for(users):
        user = await users.find_with_id(user_id)

        if user is None:
            raise NoUserError

        previous_username = user.rename(new_username=new_username)

        async with previous_username_transaction_for(previous_usernames):
            if await previous_usernames.contains_with_username(new_username):
                raise NewUsernameTakenError

            await users.update(user)
            await previous_usernames.add(previous_username)

            return Output(user=user, previous_username=previous_username)
