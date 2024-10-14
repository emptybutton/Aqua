from typing import TypeAlias

from auth.application.ports.mappers import SessionMapper
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters.repos.in_memory import InMemoryAccounts
from shared.application.ports.mappers import MapperFactory


_Session: TypeAlias = _account.internal.entities.session.Session


class InMemorySessionMapper(SessionMapper):
    def __init__(self, in_memory_accounts: InMemoryAccounts) -> None:
        self.__in_memory_accounts = in_memory_accounts

    async def add_all(self, sessions: frozenset[_Session]) -> None:
        for session in sessions:
            self.__in_memory_accounts.add_session(session)

    async def update_all(self, sessions: frozenset[_Session]) -> None:
        for session in sessions:
            self.__in_memory_accounts.update_by_session(session)


class InMemorySessionMapperFactory(MapperFactory[InMemoryAccounts, _Session]):
    def __call__(
        self, in_memory_accounts: InMemoryAccounts
    ) -> InMemorySessionMapper:
        return InMemorySessionMapper(in_memory_accounts)
