from abc import ABC, abstractmethod

from aqua.domain import entities


class Logger(ABC):
    @abstractmethod
    async def log_registered_user_registration(
        self,
        user: entities.User,
    ) -> None: ...
