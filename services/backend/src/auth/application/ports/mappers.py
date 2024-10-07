from auth.domain.models.access.aggregates import account as _account
from shared.application.ports import mappers


class AccountMapper(mappers.Mapper[_account.root.Account]): ...


class AccountNameMapper(
    mappers.Mapper[_account.internal.entities.account_name.AccountName]
): ...


class SessionMapper(mappers.Mapper[_account.internal.entities.session.Session]):
    ...
