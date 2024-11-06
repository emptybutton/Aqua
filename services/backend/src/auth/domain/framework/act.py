from abc import ABC, abstractmethod


class Act[ValueT, ResultT](ABC):
    @abstractmethod
    def __call__(self, value: ValueT) -> ResultT: ...
