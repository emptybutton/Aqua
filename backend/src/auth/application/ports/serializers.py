from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic


_DeserializedValueT = TypeVar("_DeserializedValueT")
_SerializedValueT = TypeVar("_SerializedValueT")


class AsymmetricSerializer(
    Generic[_DeserializedValueT, _SerializedValueT],
    ABC,
):
    @abstractmethod
    def serialized(self, value: _DeserializedValueT) -> _SerializedValueT: ...


class SymmetricSerializer(
    Generic[_DeserializedValueT, _SerializedValueT],
    AsymmetricSerializer[_DeserializedValueT, _SerializedValueT],
):
    @abstractmethod
    def deserialized(
        self,
        value: _SerializedValueT,
    ) -> Optional[_DeserializedValueT]: ...
