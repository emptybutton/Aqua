from typing import TypeAlias
from uuid import UUID

from auth.application.ports.views import AccountViewFrom
from auth.domain.models.access.aggregates.account.root import Account
from auth.infrastructure.adapters.repos.in_memory import InMemoryAccounts


InMemoryAccountView: TypeAlias = Account | None


class DBAccountViewFrom(AccountViewFrom[InMemoryAccounts, InMemoryAccountView]):
    async def __call__(
        self, in_memory_accounts: InMemoryAccounts, *, account_id: UUID
    ) -> InMemoryAccountView:
        return await in_memory_accounts.account_with_id(account_id)
