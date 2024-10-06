from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Never

    from shared.domain.framework.pure.entity import Entity


class Effect(ABC):
    @abstractmethod
    def consider(self, *entities: "Entity[object, Never]") -> None: ...

    @abstractmethod
    def ignore(self, *entities: "Entity[object, Never]") -> None: ...

    @abstractmethod
    def cancel(self) -> None: ...
