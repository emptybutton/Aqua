from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

from auth.domain.models.auth.pure.aggregates import account as _account


@dataclass(kw_only=True, frozen=True, slots=True)
class SessionAndPresenceOfAccountNameWithText:
    session: _account.internal.session.Session | None
    contains_account_name_with_text: bool


class Gateway(ABC):
    @abstractmethod
    async def session_with_id_and_contains_account_name_with_text(
        self,
        *,
        session_id: UUID,
        account_name_text: str,
    ) -> SessionAndPresenceOfAccountNameWithText: ...


_RepoT = TypeVar("_RepoT")


class GatewayFactory(Generic[_RepoT], ABC):
    @abstractmethod
    def __call__(self, repo: _RepoT) -> Gateway: ...
