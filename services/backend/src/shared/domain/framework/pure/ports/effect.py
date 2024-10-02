from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterator


if TYPE_CHECKING:
    from shared.domain.framework.pure.entity import Entity


class Effect(ABC):
    @abstractmethod
    def __iter__(self) -> Iterator["Entity"]: ...

    @abstractmethod
    def consider(self, *entities: "Entity") -> None: ...

    @abstractmethod
    def ignore(self, *entities: "Entity") -> None: ...

    @abstractmethod
    def cancel(self) -> None: ...

    @abstractmethod
    def clone(self) -> "Effect[Entity]": ...
