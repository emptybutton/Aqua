from abc import ABC, abstractmethod
from typing import TypeAlias

from auth.domain.models.access.aggregates import account as _account


_Account: TypeAlias = _account.root.Account
_Session: TypeAlias = _account.internal.entities.session.Session
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName


class Logger(ABC):
    @abstractmethod
    async def log_registration(
        self, *, account: _Account, session: _Session,
    ) -> None: ...

    @abstractmethod
    async def log_renaming(
        self,
        *,
        account: _Account,
        current_account_name: _AccountName,
        previous_account_name: _AccountName,
    ) -> None: ...

    @abstractmethod
    async def log_password_change(self, *, account: _Account) -> None: ...

    @abstractmethod
    async def log_login(
        self, *, account: _Account, session: _Session
    ) -> None: ...

    @abstractmethod
    async def log_session_extension(self, session: _Session) -> None: ...

    @abstractmethod
    async def log_replaced_session(self, session: _Session) -> None: ...

    @abstractmethod
    async def log_cancelled_session(self, session: _Session) -> None: ...
