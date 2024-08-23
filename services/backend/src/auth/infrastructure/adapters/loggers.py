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
