from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar, Generic
from uuid import UUID

from src.shared.application.ports.uows import UoW


@dataclass(frozen=True)
class UserRegistrationDTO:
    user_id: UUID
    username: str
    access_token: str
    refresh_token: str
    refresh_token_expiration_date: datetime


@dataclass(frozen=True)
class UserAuthenticationDTO:
    auth_user_id: UUID


UoWT_contra = TypeVar("UoWT_contra", bound=UoW[object], contravariant=True)


class Gateway(Generic[UoWT_contra], ABC):
    @abstractmethod
    async def register_user(
        self,
        name: str,
        password: str,
        *,
        uow: UoWT_contra,
    ) -> UserRegistrationDTO: ...

    @abstractmethod
    def authenticate_user(self, jwt: str) -> UserAuthenticationDTO: ...
