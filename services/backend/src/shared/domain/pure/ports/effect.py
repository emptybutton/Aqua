from abc import ABC, abstractmethod
from typing import Generic, Iterator, TypeVar


_EntityT = TypeVar("_EntityT")


class Effect(ABC, Generic[_EntityT]):
    @abstractmethod
    def __iter__(self) -> Iterator[_EntityT]: ...

    @abstractmethod
    def consider(self, *entities: _EntityT) -> None: ...

    @abstractmethod
    def ignore(self, *entities: _EntityT) -> None: ...

    @abstractmethod
    def cancel(self) -> None: ...
