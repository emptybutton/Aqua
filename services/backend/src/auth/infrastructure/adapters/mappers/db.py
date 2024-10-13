from typing import TypeAlias

from sqlalchemy import exists, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from auth.application.ports import mappers
from auth.domain.models.access.aggregates import account as _account
from shared.infrastructure.periphery.db.tables import auth as tables


_Account: TypeAlias = _account.root.Account
_Session: TypeAlias = _account.internal.entities.session.Session
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName


class DBAccountMapper(mappers.AccountMapper): ...


class DBAccountNameMapper(mappers.AccountNameMapper): ...


class DBSessionMapper(mappers.SessionMapper): ...
