from shared.domain.framework.aggregates.account.ports.low_level_spec import (
    LowLevelSpec,
)


class IsAccountNameTextTaken(LowLevelSpec[str]): ...
