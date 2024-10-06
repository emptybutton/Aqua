from dataclasses import dataclass
from datetime import 
from typing import TypeAlias, TypeVar
from uuid import UUID

from auth.application.output.log_effect import log_effect
from auth.application.ports.loggers import Logger
from auth.application.ports.repos import Accounts
from auth.domain.models.access.pure.aggregates import account as _account
from auth.domain.models.access.pure.vos.password import Password
from shared.application.adapters.effects import IndexedEffect
from shared.application.output.map_effect import map_effect
from shared.application.ports.indexes import EmptyIndexFactory
from shared.application.ports.mappers import MapperFactory
from shared.application.ports.transactions import TransactionFactory


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName
_Session: TypeAlias = _account.internal.entities.session.Session


_AccountsT = TypeVar("_AccountsT", bound=Accounts)


@dataclass(kw_only=True, frozen=True)
class Output:
    account: _Account
    previous_account_name: _AccountName


class Error(Exception): ...


class NoAccountError(Error): ...


class AccountNameTakenError(Error): ...


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
    current_time = Time(datetime_=datetime.now(UTC))
    new_username = Username(text=new_username_text)

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
            current_time=current_time,
        )

        await users.update(user)
        await previous_usernames.add(previous_username)

        await logger.log_renaming(
            user=user,
            previous_username=previous_username,
        )

        return Output(user=user, previous_username=previous_username)
