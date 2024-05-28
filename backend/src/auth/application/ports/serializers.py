from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic


_DeserializedValueT = TypeVar("_DeserializedValueT")
_SerializedValueT = TypeVar("_SerializedValueT")


class Serializer(Generic[_DeserializedValueT, _SerializedValueT], ABC):
    @abstractmethod
    def serialize(self, value: _DeserializedValueT) -> _SerializedValueT:
        ...

    @abstractmethod
    def deserialize(
        self,
        value: _SerializedValueT,
    ) -> Optional[_DeserializedValueT]:
        ...
