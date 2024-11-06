from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from auth.domain.framework.entity import AnyEntity


class Effect(ABC):
    @abstractmethod
    def consider(self, *entities: "AnyEntity") -> None: ...

    @abstractmethod
    def ignore(self, *entities: "AnyEntity") -> None: ...

    @abstractmethod
    def cancel(self) -> None: ...
