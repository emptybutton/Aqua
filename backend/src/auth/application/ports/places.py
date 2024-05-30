from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic


_Value = TypeVar("_Value")


class Place(Generic[_Value], ABC):
    @abstractmethod
    def get(self) -> Optional[_Value]:
        ...

    @abstractmethod
    def set(self, value: Optional[_Value]) -> None:
        ...
