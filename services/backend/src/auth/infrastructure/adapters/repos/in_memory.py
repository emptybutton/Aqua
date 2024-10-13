from copy import copy
from uuid import UUID

from auth.application import ports
from auth.domain.models.access.aggregates.account.root import Account
from shared.infrastructure.periphery.containers import TransactionalContainer


class InMemoryAccounts(ports.repos.Accounts, TransactionalContainer[Account]):
    async def account_with_name(
        self, *, name_text: str
    ) -> Account | None:
        for account in self._storage:
            for name in account.names:
                if name.text == name_text:
                    return copy(account)

        return None

    async def account_with_id(self, account_id: UUID) -> Account | None:
        for account in self._storage:
            if account.id == account_id:
                return copy(account)

        return None

    async def account_with_session(
        self, *, session_id: UUID
    ) -> Account | None:
        for account in self._storage:
            for session in account.sessions:
                if session.id == session_id:
                    return copy(account)

        return None

    async def contains_account_with_name(self, *, name_text: str) -> bool:
        account = self.account_with_name(name_text=name_text)

        return account is not None
