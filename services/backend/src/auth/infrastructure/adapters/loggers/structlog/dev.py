from typing import TypeAlias

from auth.application.ports import loggers
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.periphery import logs
from shared.infrastructure.periphery.structlog import dev_logger


_Account: TypeAlias = _account.root.Account
_Session: TypeAlias = _account.internal.entities.session.Session
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName


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
