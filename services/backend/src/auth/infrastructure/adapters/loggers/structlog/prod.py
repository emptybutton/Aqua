from functools import singledispatchmethod
from typing import Any, TypeAlias

from auth.application.ports import loggers
from auth.domain.framework.iterable.last_among import last_among
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.periphery import logs
from auth.infrastructure.periphery.structlog import prod_logger


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

    async def log_login(self, *, account: _Account, session: _Session) -> None:
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
        event = last_among(
            current_account_name.events_with_type(
                _account.internal.entities.account_name.BecameCurrent
            )
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
        await prod_logger.ainfo(
            logs.replaced_session_log,
            **self.__mapper.to_dict(session),
        )

    async def log_cancelled_session(self, session: _Session) -> None:
        await prod_logger.ainfo(
            logs.cancelled_session_log,
            **self.__mapper.to_dict(session),
        )
