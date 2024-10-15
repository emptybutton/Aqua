from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Any

    from shared.domain.framework.entity import Entity


class Effect(ABC):
    @abstractmethod
    def consider(self, *entities: "Entity[Any, Any]") -> None: ...

    @abstractmethod
    def ignore(self, *entities: "Entity[Any, Any]") -> None: ...

    @abstractmethod
    def cancel(self) -> None: ...
