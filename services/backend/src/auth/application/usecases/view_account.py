from typing import TypeVar
from uuid import UUID

from auth.application.ports.repos import Accounts
from auth.application.ports.views import AccountViewFrom


_AccountsT = TypeVar("_AccountsT", bound=Accounts)
_AccountViewT = TypeVar("_AccountViewT")


async def view_account(
    account_id: UUID,
    *,
    accounts: _AccountsT,
    account_view_from: AccountViewFrom[_AccountsT, _AccountViewT],
) -> _AccountViewT:
    return await account_view_from(accounts, account_id=account_id)
