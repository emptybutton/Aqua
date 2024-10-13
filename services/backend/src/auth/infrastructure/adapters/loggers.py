from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Any, TypeAlias

from auth.application.ports import loggers
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.periphery import logs
from shared.infrastructure.periphery.structlog import dev_logger, prod_logger


_Account: TypeAlias = _account.root.Account
_Session: TypeAlias = _account.internal.entities.session.Session
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName


class _Mapper:
    @singledispatchmethod
    def to_dict(self, value: object) -> dict[str, Any]:
        raise NotImplementedError

    @to_dict.register
    def _(self, account: _Account) -> dict[str, Any]:
        return dict(
            account_id=account.id,
            account_name=account.current_name.text,
        )

    @to_dict.register
    def _(self, session: _Session) -> dict[str, Any]:
        start_time = None

        if session.lifetime.start_time is not None:
            start_time = session.lifetime.start_time.datetime_

        return dict(
            session_id=session.id,
            session_account_id=session.account_id,
            session_start_time=start_time,
            session_end_time=session.lifetime.end_time.datetime_,
            session_cancelled=session.is_cancelled,
            leader_session_id=session.leader_session_id,
        )

    @to_dict.register
    def _(self, account_name: _AccountName) -> dict[str, Any]:
        taking_times = list(
            time.datetime_ for time in account_name.taking_times
        )

        return dict(
            account_name_id=account_name.id,
            account_name_account_id=account_name.account_id,
            account_name=account_name.text,
            account_name_change_times=taking_times,
        )


class StructlogDevLogger(loggers.Logger):
    async def log_registration(
        self, *, account: _Account, session: _Session
    ) -> None:
        await dev_logger.ainfo(
            logs.registration_log, account=account, session=session
        )

    async def log_login(
        self, *, account: _Account, session: _Session
    ) -> None:
        await dev_logger.ainfo(logs.login_log, account=account, session=session)

    async def log_session_extension(self, session: _Session) -> None:
        await dev_logger.ainfo(logs.session_extension_log, session=session)

    async def log_renaming(
        self,
        *,
        account: _Account,
        current_account_name: _AccountName,
        previous_account_name: _AccountName,
    ) -> None:
        await dev_logger.ainfo(
            logs.renaming_log,
            account=account,
            previous_account_name=previous_account_name,
        )

    async def log_password_change(self, *, account: _Account) -> None:
        await dev_logger.ainfo(
            logs.password_change_log,
            account=account,
        )

    async def log_replaced_session(self, session: _Session) -> None:
        await dev_logger.ainfo(logs.replaced_session_log, session=session)


class StructlogProdLogger(loggers.Logger):
    __mapper = _Mapper()

    async def log_registration(
        self, *, account: _Account, session: _Session
    ) -> None:
        await prod_logger.ainfo(
            logs.registration_log,
            **self.__mapper.to_dict(account),
            **self.__mapper.to_dict(session),
        )

    async def log_login(
        self, *, account: _Account, session: _Session
    ) -> None:
        await prod_logger.ainfo(
            logs.login_log,
            **self.__mapper.to_dict(account),
            **self.__mapper.to_dict(session),
        )

    async def log_session_extension(self, session: _Session) -> None:
        await prod_logger.ainfo(
            logs.session_extension_log, **self.__mapper.to_dict(session)
        )

    async def log_renaming(
        self,
        *,
        account: _Account,
        current_account_name: _AccountName,
        previous_account_name: _AccountName,
    ) -> None:
        event = current_account_name.last_event_with_type(
            _account.internal.entities.account_name.BecameCurrent
        )
        taking_time = None if event is None else event.new_taking_time

        await prod_logger.ainfo(
            logs.renaming_log,
            account_id=account.id,
            current_account_name_id=current_account_name.id,
            current_account_name=current_account_name.text,
            previous_account_name_id=previous_account_name.id,
            previous_account_name=previous_account_name.text,
            taking_time=taking_time,
        )

    async def log_password_change(self, *, account: _Account) -> None:
        await prod_logger.ainfo(
            logs.password_change_log,
            **self.__mapper.to_dict(account),
        )

    async def log_replaced_session(self, session: _Session) -> None:
        await dev_logger.ainfo(
            logs.replaced_session_log,
            **self.__mapper.to_dict(session),
        )


class InMemoryLogger(loggers.Logger):
    @dataclass(kw_only=True, frozen=True)
    class RegistrationLog:
        account: _Account
        session: _Session

    @dataclass(kw_only=True, frozen=True)
    class LoginLog:
        account: _Account
        session: _Session

    @dataclass(kw_only=True, frozen=True)
    class SessionExtensionLog:
        session: _Session

    @dataclass(kw_only=True, frozen=True)
    class RenamingLog:
        account: _Account
        current_account_name: _AccountName
        previous_account_name: _AccountName

    @dataclass(kw_only=True, frozen=True)
    class PasswordChangeLog:
        account: _Account

    @dataclass(kw_only=True, frozen=True)
    class ReplacedSessionLog:
        session: _Session

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
        log = InMemoryLogger.RegistrationLog(account=account, session=session)
        self.__registration_logs.append(log)

    async def log_login(
        self, *, account: _Account, session: _Session
    ) -> None:
        log = InMemoryLogger.LoginLog(account=account, session=session)
        self.__login_logs.append(log)

    async def log_session_extension(self, session: _Session) -> None:
        log = InMemoryLogger.SessionExtensionLog(session=session)
        self.__session_extension_logs.append(log)

    async def log_renaming(
        self,
        *,
        account: _Account,
        current_account_name: _AccountName,
        previous_account_name: _AccountName,
    ) -> None:
        log = InMemoryLogger.RenamingLog(
            account=account,
            current_account_name=current_account_name,
            previous_account_name=previous_account_name,
        )
        self.__renaming_logs.append(log)

    async def log_password_change(self, *, account: _Account) -> None:
        log = InMemoryLogger.PasswordChangeLog(account=account)
        self.__password_change_logs.append(log)

    async def log_replaced_session(self, session: _Session) -> None:
        log = InMemoryLogger.ReplacedSessionLog(session=session)
        self.__replaced_session_logs.append(log)
