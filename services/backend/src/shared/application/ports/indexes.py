from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from shared.domain.framework.entity import Entity, Event


_EntityT = TypeVar("_EntityT", bound=Entity)


class Index(ABC, Generic[_EntityT]):
    @property
    @abstractmethod
    def entities(self) -> frozenset[_EntityT]: ...

    @property
    @abstractmethod
    def new_entities(self) -> frozenset[_EntityT]: ...

    @property
    @abstractmethod
    def dirty_entities(self) -> frozenset[_EntityT]: ...

    @property
    @abstractmethod
    def deleted_entities(self) -> frozenset[_EntityT]: ...

    @abstractmethod
    def entities_with_event(
        self,
        *,
        event_type: type[Event],
    ) -> frozenset[_EntityT]: ...

    @abstractmethod
    def add(self, entity: _EntityT) -> None: ...

    @abstractmethod
    def remove(self, entity: _EntityT) -> None: ...


class EmptyIndexFactory(ABC, Generic[_EntityT]):
    @abstractmethod
    def __call__(self) -> Index[_EntityT]: ...
