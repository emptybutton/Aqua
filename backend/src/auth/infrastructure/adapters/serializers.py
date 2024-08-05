from datetime import datetime, UTC
from typing import TypeAlias, Optional
from uuid import UUID
import hashlib

import jwt

from auth.application.ports import serializers
from auth.domain.value_objects import (
    AccessToken,
    Password,
    PasswordHash,
    Username,
)
from auth.domain.errors import DomainError


JWT: TypeAlias = str


class AccessTokenSerializer(serializers.SymmetricSerializer[AccessToken, JWT]):
    def __init__(self, secret: str, *, algorithm: str = "HS256") -> None:
        self.__secret = secret
        self.__algorithm = algorithm

    def serialized(self, access_token: AccessToken) -> JWT:
        payload = {
            "user-id": int(access_token.user_id),
            "username": access_token.username.text,
        }

        headers = {
            "exp": access_token.expiration_date.timestamp(),
        }

        return jwt.encode(
            payload,
            self.__secret,
            headers=headers,
            algorithm=self.__algorithm,
        )

    def deserialized(
        self,
        jwt_: JWT,
    ) -> Optional[AccessToken]:
        try:
            decoded_jwt = jwt.api_jwt.decode_complete(
                jwt_,
                self.__secret,
                algorithms=[self.__algorithm],
            )
        except jwt.exceptions.InvalidTokenError:
            return None

        timestamp = decoded_jwt["header"]["exp"]

        try:
            expiration_date = datetime.fromtimestamp(timestamp, UTC)
        except Exception:
            return None

        try:
            user_id = UUID(int=decoded_jwt["payload"]["user-id"])
        except ValueError:
            return None

        try:
            return AccessToken(
                user_id,
                Username(decoded_jwt["payload"]["username"]),
                expiration_date,
            )
        except DomainError:
            return None


class PasswordSerializer(
    serializers.AsymmetricSerializer[Password, PasswordHash],
):
    def serialized(self, password: Password) -> PasswordHash:
        hash_object = hashlib.sha256()
        hash_object.update(password.text.encode("utf-8"))

        return PasswordHash(hash_object.hexdigest())
