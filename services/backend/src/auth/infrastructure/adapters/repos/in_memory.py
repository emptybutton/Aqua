from copy import deepcopy
from dataclasses import dataclass, field
from typing import Iterable, TypeAlias
from uuid import UUID

from auth.application import ports
from auth.domain.models.access.aggregates import account as _account
from shared.infrastructure.periphery.containers import TransactionalContainer


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName
_Session: TypeAlias = _account.internal.entities.session.Session


@dataclass(kw_only=True, frozen=True, slots=True)
class Storage:
    accounts: set[_Account] = field(default_factory=set)
    account_names: set[_AccountName] = field(default_factory=set)
    sessions: set[_Session] = field(default_factory=set)

    def sessions_with(self, account_id: UUID) -> Iterable[_Session]:
        for session in self.sessions:
            if session.account_id == account_id:
                yield deepcopy(session)

    def sessions_with_id(self, session_id: UUID) -> _Session | None:
        for session in self.sessions:
            if session.id == session_id:
                return deepcopy(session)

        return None

    def current_name_with(
        self, account_id: UUID
    ) -> _AccountName | None:
        for name in self.account_names:
            if name.account_id == account_id and name.is_current:
                return deepcopy(name)

        return None

    def previous_names_with(self, account_id: UUID) -> Iterable[_AccountName]:
        for name in self.account_names:
            if name.account_id == account_id and not name.is_current:
                yield deepcopy(name)


class InMemoryAccounts(ports.repos.Accounts, TransactionalContainer[Storage]):
    def __init__(self, storage: Storage | None = None) -> None:
        super().__init__()
        self._storage = Storage() if storage is None else deepcopy(storage)

    async def account_with_name(
        self, *, name_text: str
    ) -> _Account | None:
        for name in self._storage.account_names:
            if name.text == name_text:
                return self.__load_account(account_id=name.account_id)

        return None

    async def account_with_id(self, account_id: UUID) -> _Account | None:
        return self.__load_account(account_id=account_id)

    async def account_with_session(
        self, *, session_id: UUID
    ) -> _Account | None:
        for session in self._storage.sessions:
            if session.id == session_id:
                return self.__load_account(account_id=session.account_id)

        return None

    async def contains_account_with_name(self, *, name_text: str) -> bool:
        for account_name in self._storage.account_names:
            if account_name.text == name_text:
                return True

        return False

    def add_account(self, account: _Account) -> None:
        self._storage.accounts.add(deepcopy(account))

    def add_account_name(self, account_name: _AccountName) -> None:
        self._storage.account_names.add(deepcopy(account_name))

    def add_session(self, session: _Session) -> None:
        self._storage.sessions.add(deepcopy(session))

    def update_by_account(self, account: _Account) -> None:
        for stored_account in set(self._storage.accounts):
            if account.id == stored_account.id:
                self._storage.accounts.remove(stored_account)
                self._storage.accounts.add(account)
                return

    def update_by_session(self, session: _Session) -> None:
        for stored_session in set(self._storage.sessions):
            if session.id == stored_session.id:
                self._storage.sessions.remove(stored_session)
                self._storage.sessions.add(session)
                return

    def update_by_account_name(self, account_name: _AccountName) -> None:
        for stored_account_name in set(self._storage.account_names):
            if account_name.id == stored_account_name.id:
                self._storage.account_names.remove(stored_account_name)
                self._storage.account_names.add(account_name)
                return

    def __load_account(self, *, account_id: UUID) -> _Account | None:
        for account in self._storage.accounts:
            if account.id == account_id:
                return self.__load_account_with_associations(account)

        return None

    def __load_account_with_associations(
        self, account: _Account
    ) -> _Account | None:
        current_name = self._storage.current_name_with(account.id)

        if current_name is None:
            return None

        return _Account(
            id=account.id,
            current_name=current_name,
            previous_names=set(self._storage.previous_names_with(account.id)),
            sessions=set(self._storage.sessions_with(account.id)),
            password_hash=account.password_hash,
            events=list(),
        )
