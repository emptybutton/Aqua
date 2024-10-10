from auth.application.ports import mappers


class DBAccountMapper(mappers.AccountMapper): ...


class DBAccountNameMapper(mappers.AccountNameMapper): ...


class DBSessionMapper(mappers.SessionMapper):
    ...
