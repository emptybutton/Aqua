from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeAlias, TypeVar
from uuid import UUID

from auth.domain.models.access.aggregates import account as _account


_Account: TypeAlias = _account.root.Account
_Session: TypeAlias = _account.internal.entities.session.Session


@dataclass(kw_only=True, frozen=True, slots=True)
class SessionAndPresenceOfAccountNameWithText:
    session: _Session | None
    contains_account_name_with_text: bool


@dataclass(kw_only=True, frozen=True, slots=True)
class SessionAndAccount:
    session: _Session | None
    account: _Account | None


@dataclass(kw_only=True, frozen=True, slots=True)
class AccountAndPresenceOfAccountNameWithText:
    account: _Account | None
    contains_account_name_with_text: bool


class Gateway(ABC):
    @abstractmethod
    async def session_with_id_and_contains_account_name_with_text(
        self,
        *,
        session_id: UUID,
        account_name_text: str,
    ) -> SessionAndPresenceOfAccountNameWithText: ...

    @abstractmethod
    async def session_with_id_and_account_with_name(
        self, *, session_id: UUID, account_name_text: str
    ) -> SessionAndAccount: ...

    @abstractmethod
    async def session_with_id(self, session_id: UUID) -> _Session | None: ...

    @abstractmethod
    async def account_with_id_and_contains_account_name_with_text(
        self,
        *,
        account_id: UUID,
        account_name_text: str,
    ) -> AccountAndPresenceOfAccountNameWithText: ...


_RepoT = TypeVar("_RepoT")


class GatewayFactory(Generic[_RepoT], ABC):
    @abstractmethod
    def __call__(self, repo: _RepoT) -> Gateway: ...
