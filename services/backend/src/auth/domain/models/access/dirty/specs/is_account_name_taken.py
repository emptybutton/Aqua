from typing import TypeAlias

from auth.domain.models.access.dirty.ports.specs import (
    is_account_name_text_taken as _is_account_name_text_taken,
)
from auth.domain.models.auth.aggregates.account.internal import (
    account_name as _account_name,
)
from shared.domain.framework.dirty.high_level_spec import HighLevelSpec


_IsAccountNameTextTaken: TypeAlias = (
    _is_account_name_text_taken.IsAccountNameTextTaken
)


class IsAccountNameTaken(HighLevelSpec[_account_name.AccountName]):
    def __init__(
        self,
        is_account_name_text_taken: _IsAccountNameTextTaken,
    ) -> None:
        self.__is_account_name_text_taken = is_account_name_text_taken

    async def __call__(self, account_name: _account_name.AccountName) -> bool:
        return self.__is_account_name_text_taken(account_name.text)
