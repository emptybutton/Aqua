from auth.domain.models.auth.pure.aggregates import account as _account
from shared.application.ports import mappers


class AccountMapper(mappers.Mapper[_account.root.Account]): ...


class AccountNameMapper(
    mappers.Mapper[_account.internal.account_name.AccountName]
): ...


class SessionMapper(mappers.Mapper[_account.internal.session.Session]): ...
