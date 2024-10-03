from abc import ABC, abstractmethod
from uuid import UUID

from auth.domain.models.access.pure.aggregates.account.root import Account


class Accounts(ABC):
    @abstractmethod
    async def account_with_id(self, account_id: UUID) -> Account | None: ...

    @abstractmethod
    async def account_with_session(
        self, *, session_id: UUID
    ) -> Account | None: ...

    @abstractmethod
    async def contains_account_with_name(self, *, name_text: str) -> bool: ...
