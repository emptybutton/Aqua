from abc import ABC, abstractmethod

from auth.domain.models.access.pure.aggregates import account as _account


class Logger(ABC):
    @abstractmethod
    async def log_registration(
        self,
        *,
        account: _account.root.Account,
        session: _account.internal.session.Session,
    ) -> None: ...

    @abstractmethod
    async def log_renaming(
        self,
        *,
        account: _account.root.Account,
        previous_account_name: _account.internal.account_name.AccountName,
    ) -> None: ...

    @abstractmethod
    async def log_password_change(
        self,
        *,
        account: _account.root.Account,
        current_session: _account.internal.session.Session,
        canceled_sessions: frozenset[_account.internal.session.Session],
    ) -> None: ...

    @abstractmethod
    async def log_login(
        self,
        *,
        account: _account.root.Account,
        current_session: _account.internal.session.Session,
    ) -> None: ...

    @abstractmethod
    async def log_session_extension(
        self, session: _account.internal.session.Session
    ) -> None: ...

    @abstractmethod
    async def log_replaced_session(
        self, session: _account.internal.session.Session
    ) -> None: ...
