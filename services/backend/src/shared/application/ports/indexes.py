from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from shared.domain.framework.entity import Entity, EntityEvent


_EntityT = TypeVar("_EntityT", bound=Entity[Any, Any])


class Index(Generic[_EntityT], ABC):
    @property
    @abstractmethod
    def entities(self) -> frozenset[_EntityT]: ...

    @property
    @abstractmethod
    def new_entities(self) -> frozenset[_EntityT]: ...

    @property
    @abstractmethod
    def dirty_entities(self) -> frozenset[_EntityT]: ...

    @abstractmethod
    def entities_with_event(
        self,
        *,
        event_type: type[EntityEvent[Any]],
    ) -> frozenset[_EntityT]: ...

    @abstractmethod
    def add(self, entity: _EntityT) -> None: ...

    @abstractmethod
    def remove(self, entity: _EntityT) -> None: ...


class EmptyIndexFactory(ABC):
    @abstractmethod
    def __call__(self, entity_type: type[_EntityT]) -> Index[_EntityT]: ...
