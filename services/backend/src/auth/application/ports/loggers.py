from abc import ABC, abstractmethod

from auth.domain import entities


class Logger(ABC):
    @abstractmethod
    async def log_registration(
        self, *, user: entities.User, session: entities.Session
    ) -> None: ...

    @abstractmethod
    async def log_renaming(
        self,
        *,
        user: entities.User,
        previous_username: entities.PreviousUsername,
    ) -> None: ...

    @abstractmethod
    async def log_password_change(
        self,
        *,
        user: entities.User,
        other_sessions: tuple[entities.Session, ...],
    ) -> None: ...

    @abstractmethod
    async def log_login(
        self, *, user: entities.User, session: entities.Session
    ) -> None: ...

    @abstractmethod
    async def log_session_extension(
        self, session: entities.Session
    ) -> None: ...
