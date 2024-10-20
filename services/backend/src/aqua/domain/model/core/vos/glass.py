from dataclasses import dataclass

from aqua.domain.model.primitives.vos.water import Water


@dataclass(kw_only=True, frozen=True, slots=True)
class Glass:
    capacity: Water
