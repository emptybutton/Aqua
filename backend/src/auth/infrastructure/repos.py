from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.application.ports import repos
from src.auth.domain import entities, value_objects
from src.shared.infrastructure.db import models


class Users(repos.Users):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def add(self, user: entities.User) -> None:
        pass

    def get_by_name(
        self, username: value_objects.Username
    ) -> Optional[entities.User]:
        query = (
            select(models.User.id, models.User.name, models.User.password_hash)
            .where(models.User.name == username.text)
        )
        row_user = self.__session.execute(query).first()

        if row_user is None:
            return None

        return entities.User(
            id=row_user.id,
            name=value_objects.Username(row_user.name),
            password_hash=value_objects.PasswordHash(row_user.password_hash),
        )

    def has_with_name(self, username: value_objects.Username) -> bool:
        query = (
            select(models.User)
            .where(models.User.name == username.text)
            .exists()
        )

        result: bool = self.__session.execute(query).scalar()  # type: ignore[call-overload]
        return result
