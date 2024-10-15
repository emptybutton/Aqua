from typing import TypeAlias

from auth.application.ports.mappers import AccountMapper
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters.repos.in_memory import InMemoryAccounts
from shared.application.ports.mappers import MapperFactory


_Account: TypeAlias = _account.root.Account


class InMemoryAccountMapper(AccountMapper):
    def __init__(self, in_memory_accounts: InMemoryAccounts) -> None:
        self.__in_memory_accounts = in_memory_accounts

    async def add_all(self, accounts: frozenset[_Account]) -> None:
        for account in accounts:
            self.__in_memory_accounts.add_account(account)

    async def update_all(self, accounts: frozenset[_Account]) -> None:
        for account in accounts:
            self.__in_memory_accounts.update_by_account(account)


class InMemoryAccountMapperFactory(MapperFactory[InMemoryAccounts, _Account]):
    def __call__(
        self, in_memory_accounts: InMemoryAccounts
    ) -> InMemoryAccountMapper:
        return InMemoryAccountMapper(in_memory_accounts)
