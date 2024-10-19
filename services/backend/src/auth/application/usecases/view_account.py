from uuid import UUID

from auth.application.ports.repos import Accounts
from auth.application.ports.views import AccountViewFrom


async def view_account[AccountsT: Accounts, AccountViewT](
    account_id: UUID,
    *,
    accounts: AccountsT,
    account_view_from: AccountViewFrom[AccountsT, AccountViewT],
) -> AccountViewT:
    return await account_view_from(accounts, account_id=account_id)
