from auth.domain.models.auth.aggregates.account.internal import (
    account_name as _account_name,
)
from shared.domain.framework.dirty.high_level_spec import HighLevelSpec
from shared.domain.framework.dirty.ports.low_level_spec import LowLevelSpec


class IsAccountNameTaken(HighLevelSpec[_account_name.AccountName]):
    def __init__(self, is_account_name_text_unique: LowLevelSpec[str]) -> None:
        self.__is_account_name_text_unique = is_account_name_text_unique

    async def __call__(self, account_name: _account_name.AccountName) -> bool:
        return self.__is_account_name_text_unique(account_name.text)
