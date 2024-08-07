from abc import ABC, abstractmethod
from typing import TypeVar, Generic


_DeserializedValueT = TypeVar("_DeserializedValueT")
_SerializedValueT = TypeVar("_SerializedValueT")


class AsymmetricSerializer(
    Generic[_DeserializedValueT, _SerializedValueT],
    ABC,
):
    @abstractmethod
    def serialized(self, value: _DeserializedValueT) -> _SerializedValueT: ...


class SecureSymmetricSerializer(
    Generic[_DeserializedValueT, _SerializedValueT],
    AsymmetricSerializer[_DeserializedValueT, _SerializedValueT],
):
    @abstractmethod
    def deserialized(
        self,
        value: _SerializedValueT,
    ) -> _DeserializedValueT | None: ...
