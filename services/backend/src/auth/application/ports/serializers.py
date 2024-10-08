from abc import ABC, abstractmethod
from typing import Generic, TypeVar


_DeserializedValueT = TypeVar("_DeserializedValueT")
_SerializedValueT = TypeVar("_SerializedValueT")


class AsymmetricSerializer(
    Generic[_DeserializedValueT, _SerializedValueT], ABC
):
    @abstractmethod
    def serialized(self, value: _DeserializedValueT) -> _SerializedValueT: ...
