from typing import TypeAlias

from auth.application.ports.mappers import AccountNameMapper
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters.repos.in_memory import InMemoryAccounts
from shared.application.ports.mappers import MapperFactory


_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName


class InMemoryAccountNameMapper(AccountNameMapper):
    def __init__(self, in_memory_accounts: InMemoryAccounts) -> None:
        self.__in_memory_accounts = in_memory_accounts

    async def add_all(self, account_names: frozenset[_AccountName]) -> None:
        for name in account_names:
            self.__in_memory_accounts.add_account_name(name)

    async def update_all(self, account_names: frozenset[_AccountName]) -> None:
        for name in account_names:
            self.__in_memory_accounts.update_by_account_name(name)


class InMemoryAccountNameMapperFactory(
    MapperFactory[InMemoryAccounts, _AccountName]
):
    def __call__(
        self, in_memory_accounts: InMemoryAccounts
    ) -> InMemoryAccountNameMapper:
        return InMemoryAccountNameMapper(in_memory_accounts)
