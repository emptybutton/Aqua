from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypeAlias, TypeVar
from uuid import UUID

from auth.application.output.log_effect import log_effect
from auth.application.ports.gateway import GatewayFactory
from auth.application.ports.loggers import Logger
from auth.application.ports.repos import Accounts
from auth.domain.models.access.pure.aggregates import account as _account
from auth.domain.models.access.pure.vos.password import Password
from auth.domain.models.access.pure.vos.time import Time
from shared.application.adapters.effects import IndexedEffect
from shared.application.output.map_effect import map_effect
from shared.application.ports.indexes import EmptyIndexFactory
from shared.application.ports.mappers import MapperFactory
from shared.application.ports.transactions import TransactionFactory


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.account_name.AccountName
_Session: TypeAlias = _account.internal.session.Session


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    account: _Account
    session: _Session


class Error(Exception): ...


class NoAccountError(Error): ...


class IncorrectPasswordError(Error): ...


_AccountsT = TypeVar("_AccountsT", bound=Accounts)


async def login_to_account(
    session_id: UUID | None,
    name_text: str,
    password_text: str,
    *,
    empty_index_factory: EmptyIndexFactory,
    accounts: _AccountsT,
    account_mapper_in: MapperFactory[_AccountsT, _Account],
    account_name_mapper_in: MapperFactory[_AccountsT, _AccountName],
    session_mapper_in: MapperFactory[_AccountsT, _Session],
    transaction_for: TransactionFactory[_AccountsT],
    gateway_to: GatewayFactory[_AccountsT],
    logger: Logger,
) -> Output:
    current_time = Time(datetime_=datetime.now(UTC))

    try:
        password = Password(text=password_text)
    except Password.Error as error:
        raise IncorrectPasswordError from error

    async with transaction_for(accounts):
        if session_id is None:
            current_session = None
            account = await accounts.account_with_name(name_text=name_text)
        else:
            gateway = gateway_to(accounts)
            gateway_result = (
                await gateway.session_with_id_and_account_with_name(
                    session_id=session_id,
                    name_text=name_text,
                )
            )
            current_session = gateway_result.session
            account = gateway_result.account

        effect = IndexedEffect(empty_index_factory=empty_index_factory)

        try:
            session = _account.root.login_to(
                account,
                password=password,
                current_time=current_time,
                current_session=current_session,
                effect=effect,
            )
        except _Account.InvalidPasswordHashForPrimaryAuthenticationError as err:
            raise IncorrectPasswordError from err

        await logger.log_login(account=account, session=session)

        await log_effect(effect, logger)
        await map_effect(effect, {
            _Account: account_mapper_in(accounts),
            _AccountName: account_name_mapper_in(accounts),
            _Session: session_mapper_in(accounts),
        })

        return Output(account=account, session=session)
