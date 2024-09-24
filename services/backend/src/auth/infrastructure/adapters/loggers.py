from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Any

from auth.application.ports import loggers
from auth.domain import entities
from auth.infrastructure.periphery import logs
from shared.infrastructure.periphery.structlog import dev_logger, prod_logger


class _Mapper:
    @singledispatchmethod
    def to_dict(self, value: object) -> dict[str, Any]:
        raise NotImplementedError

    @to_dict.register
    def _(self, user: entities.User) -> dict[str, Any]:
        return dict(user_id=user.id, username=user.name)

    @to_dict.register
    def _(self, session: entities.Session) -> dict[str, Any]:
        start_time = None

        if session.lifetime.start_time is not None:
            start_time = session.lifetime.start_time.datetime_

        return dict(
            session_id=session.id,
            session_user_id=session.user_id,
            session_start_time=start_time,
            session_end_time=session.lifetime.end_time.datetime_,
            session_cancelled=session.is_cancelled,
            next_session_id=session.next_session_id,
        )

    @to_dict.register
    def _(self, previous_username: entities.PreviousUsername) -> dict[str, Any]:
        change_time = None

        if previous_username.change_time is not None:
            change_time = previous_username.change_time.datetime_

        return dict(
            previous_username_id=previous_username.id,
            previous_username_user_id=previous_username.user_id,
            previous_username=previous_username.username,
            username_change_time=change_time,
        )


class StructlogDevLogger(loggers.Logger):
    async def log_registration(
        self, *, user: entities.User, session: entities.Session
    ) -> None:
        await dev_logger.ainfo(
            logs.registration_log, user=user, session=session
        )

    async def log_login(
        self, *, user: entities.User, session: entities.Session
    ) -> None:
        await dev_logger.ainfo(logs.login_log, user=user, session=session)

    async def log_session_extension(self, session: entities.Session) -> None:
        await dev_logger.ainfo(logs.session_extension_log, session=session)

    async def log_renaming(
        self,
        *,
        user: entities.User,
        previous_username: entities.PreviousUsername,
    ) -> None:
        await dev_logger.ainfo(
            logs.renaming_log,
            user=user,
            previous_username=previous_username,
        )

    async def log_password_change(
        self,
        *,
        user: entities.User,
        other_sessions: tuple[entities.Session, ...],
    ) -> None:
        await dev_logger.ainfo(
            logs.password_change_log,
            user=user,
            other_sessions=other_sessions,
        )

    async def log_replaced_session(self, session: entities.Session) -> None:
        await dev_logger.ainfo(logs.replaced_session_log, session=session)


class StructlogProdLogger(loggers.Logger):
    __mapper = _Mapper()

    async def log_registration(
        self, *, user: entities.User, session: entities.Session
    ) -> None:
        await prod_logger.ainfo(
            logs.registration_log,
            **self.__mapper.to_dict(user),
            **self.__mapper.to_dict(session),
        )

    async def log_login(
        self, *, user: entities.User, session: entities.Session
    ) -> None:
        await prod_logger.ainfo(
            logs.login_log,
            **self.__mapper.to_dict(user),
            **self.__mapper.to_dict(session),
        )

    async def log_session_extension(self, session: entities.Session) -> None:
        await prod_logger.ainfo(
            logs.session_extension_log, **self.__mapper.to_dict(session)
        )

    async def log_renaming(
        self,
        *,
        user: entities.User,
        previous_username: entities.PreviousUsername,
    ) -> None:
        change_time = None

        if previous_username.change_time is not None:
            change_time = previous_username.change_time.datetime_

        await prod_logger.ainfo(
            logs.renaming_log,
            user_id=user.id,
            new_username=user.name,
            previous_username=previous_username.username,
            previous_username_id=previous_username.id,
            username_change_time=change_time,
        )

    async def log_password_change(
        self,
        *,
        user: entities.User,
        other_sessions: tuple[entities.Session, ...],
    ) -> None:
        await prod_logger.ainfo(
            logs.password_change_log,
            **self.__mapper.to_dict(user),
            other_sessions=tuple(map(self.__mapper.to_dict, other_sessions)),
        )

    async def log_replaced_session(self, session: entities.Session) -> None:
        await dev_logger.ainfo(
            logs.replaced_session_log,
            **self.__mapper.to_dict(session),
        )


class InMemoryStorageLogger(loggers.Logger):
    @dataclass(kw_only=True, frozen=True)
    class RegistrationLog:
        user: entities.User
        session: entities.Session

    @dataclass(kw_only=True, frozen=True)
    class LoginLog:
        user: entities.User
        session: entities.Session

    @dataclass(kw_only=True, frozen=True)
    class SessionExtensionLog:
        session: entities.Session

    @dataclass(kw_only=True, frozen=True)
    class RenamingLog:
        user: entities.User
        previous_username: entities.PreviousUsername

    @dataclass(kw_only=True, frozen=True)
    class PasswordChangeLog:
        user: entities.User
        other_sessions: tuple[entities.Session, ...]

    @dataclass(kw_only=True, frozen=True)
    class ReplacedSessionLog:
        session: entities.Session

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
        self, *, user: entities.User, session: entities.Session
    ) -> None:
        log = InMemoryStorageLogger.RegistrationLog(user=user, session=session)
        self.__registration_logs.append(log)

    async def log_login(
        self, *, user: entities.User, session: entities.Session
    ) -> None:
        log = InMemoryStorageLogger.LoginLog(user=user, session=session)
        self.__login_logs.append(log)

    async def log_session_extension(self, session: entities.Session) -> None:
        log = InMemoryStorageLogger.SessionExtensionLog(session=session)
        self.__session_extension_logs.append(log)

    async def log_renaming(
        self,
        *,
        user: entities.User,
        previous_username: entities.PreviousUsername,
    ) -> None:
        log = InMemoryStorageLogger.RenamingLog(
            user=user,
            previous_username=previous_username,
        )
        self.__renaming_logs.append(log)

    async def log_password_change(
        self,
        *,
        user: entities.User,
        other_sessions: tuple[entities.Session, ...],
    ) -> None:
        log = InMemoryStorageLogger.PasswordChangeLog(
            user=user,
            other_sessions=other_sessions,
        )
        self.__password_change_logs.append(log)

    async def log_replaced_session(self, session: entities.Session) -> None:
        log = InMemoryStorageLogger.ReplacedSessionLog(session=session)
        self.__replaced_session_logs.append(log)
