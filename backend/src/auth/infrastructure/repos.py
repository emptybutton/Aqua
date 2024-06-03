from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.domain import entities
from src.auth.domain import value_objects
from src.auth.infrastructure.converters import Entities
from src.shared.infrastructure.db import models


class Users:
    def __init__(self, session: Session) -> None:
        self.__session = session

    def add(self, user: entities.User) -> None:
        pass

    def get_by_name(
        self, username: value_objects.Username
    ) -> Optional[entities.User]:
        stmt = select(models.User).where(models.User.name == username.text)
        user_model = self.__session.scalars(stmt).first()

        return None if user_model is None else Entities.user_of(user_model)

    def has_with_name(self, username: value_objects.Username) -> bool:
        stmt = (
            select(models.User)
            .where(models.User.name == username.text)
            .exists()
        )

        return self.__session.scalar(stmt).first()
