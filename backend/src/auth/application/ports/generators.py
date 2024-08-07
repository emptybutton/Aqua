from abc import ABC, abstractmethod


class GenerateHighEntropyText(ABC):
    @abstractmethod
    def __call__(self) -> str: ...
