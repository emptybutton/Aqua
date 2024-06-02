from src.auth.domain import entities
from src.auth.domain import value_objects
from src.shared.infrastructure.db import models


class Entities:
    @staticmethod
    def user_of(user_model: models.User) -> entities.User:
        return entities.User(
            id=user_model.id,
            name=value_objects.Username(user_model.name),
            password_hash=value_objects.PasswordHash(user_model.password_hash),
        )
