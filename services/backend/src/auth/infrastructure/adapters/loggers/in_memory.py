from dataclasses import dataclass
from typing import TypeAlias

from auth.application.ports import loggers
from auth.domain.models.access.aggregates import account as _account


_Account: TypeAlias = _account.root.Account
_Session: TypeAlias = _account.internal.entities.session.Session
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName


@dataclass(kw_only=True, frozen=True, slots=True)
class RegistrationLog:
    account: _Account
    session: _Session


@dataclass(kw_only=True, frozen=True, slots=True)
class LoginLog:
    account: _Account
    session: _Session


@dataclass(kw_only=True, frozen=True, slots=True)
class SessionExtensionLog:
    session: _Session


@dataclass(kw_only=True, frozen=True, slots=True)
class RenamingLog:
    account: _Account
    current_account_name: _AccountName
    previous_account_name: _AccountName


@dataclass(kw_only=True, frozen=True, slots=True)
class PasswordChangeLog:
    account: _Account


@dataclass(kw_only=True, frozen=True, slots=True)
class ReplacedSessionLog:
    session: _Session


class InMemoryLogger(loggers.Logger):
    __registration_logs: list[RegistrationLog]
    __login_logs: list[LoginLog]
    __session_extension_logs: list[SessionExtensionLog]
    __renaming_logs: list[RenamingLog]
    __password_change_logs: list[PasswordChangeLog]
    __replaced_session_logs: list[ReplacedSessionLog]

    def __init__(self) -> None:
        self.__registration_logs = list()
        self.__login_logs = list()
        self.__session_extension_logs = list()
        self.__renaming_logs = list()
        self.__password_change_logs = list()
        self.__replaced_session_logs = list()

    @property
    def registration_logs(self) -> list[RegistrationLog]:
        return list(self.__registration_logs)

    @property
    def login_logs(self) -> list[LoginLog]:
        return list(self.__login_logs)

    @property
    def session_extension_logs(self) -> list[SessionExtensionLog]:
        return list(self.__session_extension_logs)

    @property
    def renaming_logs(self) -> list[RenamingLog]:
        return list(self.__renaming_logs)

    @property
    def password_change_logs(self) -> list[PasswordChangeLog]:
        return list(self.__password_change_logs)

    @property
    def replaced_session_logs(self) -> list[ReplacedSessionLog]:
        return list(self.__replaced_session_logs)

    @property
    def is_empty(self) -> bool:
        return (
            not self.__registration_logs
            and not self.__login_logs
            and not self.__session_extension_logs
            and not self.__renaming_logs
            and not self.__password_change_logs
            and not self.__replaced_session_logs
        )

    async def log_registration(
        self, *, account: _Account, session: _Session
    ) -> None:
        log = RegistrationLog(account=account, session=session)
        self.__registration_logs.append(log)

    async def log_login(
        self, *, account: _Account, session: _Session
    ) -> None:
        log = LoginLog(account=account, session=session)
        self.__login_logs.append(log)

    async def log_session_extension(self, session: _Session) -> None:
        log = SessionExtensionLog(session=session)
        self.__session_extension_logs.append(log)

    async def log_renaming(
        self,
        *,
        account: _Account,
        current_account_name: _AccountName,
        previous_account_name: _AccountName,
    ) -> None:
        log = RenamingLog(
            account=account,
            current_account_name=current_account_name,
            previous_account_name=previous_account_name,
        )
        self.__renaming_logs.append(log)

    async def log_password_change(self, *, account: _Account) -> None:
        log = PasswordChangeLog(account=account)
        self.__password_change_logs.append(log)

    async def log_replaced_session(self, session: _Session) -> None:
        log = ReplacedSessionLog(session=session)
        self.__replaced_session_logs.append(log)
