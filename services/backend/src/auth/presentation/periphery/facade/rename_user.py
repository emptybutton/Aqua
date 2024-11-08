from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, TypeAlias
from uuid import UUID

from result import Err, Ok

from auth.application import ports
from auth.application.usecases.change_account_name import (
    change_account_name as _change_account_name,
)
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters import (
    gateways,
    mappers,
    repos,
)
from auth.infrastructure.adapters.transactions import (
    DBConnectionTransactionFactory,
)
from auth.presentation.di.containers import async_container


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user_id: UUID
    new_username: str
    previous_username: str


class Error(Exception): ...


class NoUserError(Error): ...


class NewUsernameTakenError(Error): ...


class EmptyUsernameError(Error): ...


@asynccontextmanager
async def perform(user_id: UUID, new_username: str) -> AsyncIterator[Output]:
    async with async_container() as container, _change_account_name(
        user_id,
        new_username,
        accounts=await container.get(repos.db.DBAccounts, "repos"),
        account_mapper_in=await container.get(
            mappers.db.account.DBAccountMapperFactory, "mappers"
        ),
        account_name_mapper_in=await container.get(
            mappers.db.account_name.DBAccountNameMapperFactory, "mappers"
        ),
        session_mapper_in=await container.get(
            mappers.db.session.DBSessionMapperFactory, "mappers"
        ),
        transaction_for=await container.get(
            DBConnectionTransactionFactory, "transactions"
        ),
        gateway_to=await container.get(
            gateways.db.DBGatewayFactory, "gateways"
        ),
        logger=await container.get(ports.loggers.Logger, "loggers"),
    ) as result:
        match result:
            case Ok(output):
                previous_username_text = output.account.current_name.text

                if output.previous_account_name is not None:
                    previous_username_text = output.previous_account_name.text

                yield Output(
                    user_id=output.account.id,
                    new_username=output.account.current_name.text,
                    previous_username=previous_username_text,
                )
            case Err("no_account"):
                raise NoUserError
            case Err("account_name_text_is_empty"):
                raise EmptyUsernameError
            case Err("account_name_is_taken"):
                raise NewUsernameTakenError
            case _:
                raise Error
