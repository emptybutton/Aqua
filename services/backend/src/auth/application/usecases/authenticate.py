from datetime import UTC, datetime
from typing import TypeAlias, TypeVar
from uuid import UUID

from auth.application.output.log_effect import log_effect
from auth.application.ports.loggers import Logger
from auth.application.ports.repos import Accounts
from auth.domain.models.access.pure.aggregates import account as _account
from auth.domain.models.access.pure.vos.time import Time
from shared.application.adapters.effects import IndexedEffect
from shared.application.output.map_effect import map_effect
from shared.application.ports.indexes import EmptyIndexFactory
from shared.application.ports.mappers import MapperFactory
from shared.application.ports.transactions import TransactionFactory


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.account_name.AccountName
_Session: TypeAlias = _account.internal.session.Session


class Error(Exception): ...


class NoAccountError(Error): ...


_AccountsT = TypeVar("_AccountsT", bound=Accounts)


async def authenticate(
    session_id: UUID,
    *,
    empty_index_factory: EmptyIndexFactory,
    accounts: _AccountsT,
    account_mapper_in: MapperFactory[_AccountsT, _Account],
    account_name_mapper_in: MapperFactory[_AccountsT, _AccountName],
    session_mapper_in: MapperFactory[_AccountsT, _Session],
    transaction_for: TransactionFactory[_AccountsT],
    logger: Logger,
) -> _Session:
    current_time = Time(datetime_=datetime.now(UTC))

    async with transaction_for(accounts):
        account = await accounts.account_with_session(session_id=session_id)

        if account is None:
            raise NoAccountError

        effect = IndexedEffect(empty_index_factory=empty_index_factory)
        session = account.secondarily_authenticate(
            session_id=session_id, current_time=current_time, effect=effect
        )

        await log_effect(effect, logger)
        await map_effect(effect, {
            _Account: account_mapper_in(accounts),
            _AccountName: account_name_mapper_in(accounts),
            _Session: session_mapper_in(accounts),
        })

        return session
