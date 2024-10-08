from auth.application.ports import mappers


class AccountMapper(mappers.Mapper[_account.root.Account]): ...


class AccountNameMapper(
    mappers.Mapper[_account.internal.entities.account_name.AccountName]
): ...


class SessionMapper(mappers.Mapper[_account.internal.entities.session.Session]):
    ...
