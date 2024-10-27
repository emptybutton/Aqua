from aqua.domain.framework.entity import AnyEntity
from aqua.domain.framework.fp.act import Act


class HighLevelSpec[EntityT: AnyEntity](Act[EntityT, bool]): ...
