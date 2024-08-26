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
        return dict(
            session_id=session.id,
            session_user_id=session.user_id,
            session_start_time=session.lifetime.start_time,
            session_end_time=session.lifetime.end_time,
        )


class StructlogDevLogger(loggers.Logger):
    async def log_registration(
        self,
        *,
        user: entities.User,
        session: entities.Session,
    ) -> None:
        await dev_logger.ainfo(
            logs.registration_log,
            user=user,
            session=session,
        )

    async def log_login(
        self,
        *,
        user: entities.User,
        session: entities.Session,
    ) -> None:
        await dev_logger.ainfo(logs.login_log, user=user, session=session)

    async def log_session_extension(
        self,
        session: entities.Session,
    ) -> None:
        await dev_logger.ainfo(logs.login_log, session=session)


class StructlogProdLogger(loggers.Logger):
    __mapper = _Mapper()

    async def log_registration(
        self,
        *,
        user: entities.User,
        session: entities.Session,
    ) -> None:
        await prod_logger.ainfo(
            logs.registration_log,
            **self.__mapper.to_dict(user),
            **self.__mapper.to_dict(session),
        )

    async def log_login(
        self,
        *,
        user: entities.User,
        session: entities.Session,
    ) -> None:
        await prod_logger.ainfo(
            logs.login_log,
            **self.__mapper.to_dict(user),
            **self.__mapper.to_dict(session),
        )

    async def log_session_extension(
        self,
        session: entities.Session,
    ) -> None:
        await prod_logger.ainfo(
            logs.login_log,
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

    __registration_logs: list[RegistrationLog]
    __login_logs: list[LoginLog]
    __session_extension_logs: list[SessionExtensionLog]

    def __init__(self) -> None:
        self.__registration_logs = list()
        self.__login_logs = list()
        self.__session_extension_logs = list()

    @property
    def registration_logs(self) -> list[RegistrationLog]:
        return list(self.__registration_logs)

    @property
    def login_logs(self) -> list[LoginLog]:
        return list(self.__login_logs)

    @property
    def session_extension_logs(self) -> list[SessionExtensionLog]:
        return list(self.__session_extension_logs)

    async def log_registration(
        self,
        *,
        user: entities.User,
        session: entities.Session,
    ) -> None:
        log = InMemoryStorageLogger.RegistrationLog(user=user, session=session)
        self.__registration_logs.append(log)

    async def log_login(
        self,
        *,
        user: entities.User,
        session: entities.Session,
    ) -> None:
        log = InMemoryStorageLogger.LoginLog(user=user, session=session)
        self.__login_logs.append(log)

    async def log_session_extension(
        self,
        session: entities.Session,
    ) -> None:
        log = InMemoryStorageLogger.SessionExtensionLog(session=session)
        self.__session_extension_logs.append(log)
