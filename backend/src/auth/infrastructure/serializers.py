from typing import TypeAlias, Optional
import hashlib

import jwt

from src.auth.domain.value_objects import AccessToken, Password, PasswordHash
from src.auth.application.ports import serializers


JWT: TypeAlias = str


class AccessTokenSerializer(serializers.SymmetricSerializer[AccessToken, JWT]):
    def __init__(self, secret: str) -> None:
        self.__secret = secret

    def serialized(self, access_token: AccessToken) -> JWT:
        payload = {
            "user-id": access_token.user_id,
            "username": access_token.username.text,
        }

        headers = {
            "exp": access_token.expiration_date.timestamp(),
        }

        return jwt.encode(payload, self.__secret, headers=headers)

    def deserialized(
        self,
        jwt_: JWT,
    ) -> Optional[AccessToken]:
        try:
            decoded_jwt = jwt.api_jwt.decode_complete(jwt_, self.__secret)
        except jwt.exceptions.InvalidTokenError:
            return None

        return AccessToken(
            decoded_jwt["payload"]["user-id"],
            decoded_jwt["payload"]["username"],
            decoded_jwt["header"]["exp"],
        )


class PasswordSerializer(
    serializers.AsymmetricSerializer[Password, PasswordHash],
):
    def serialized(self, password: Password) -> PasswordHash:
        hash_object = hashlib.sha256()
        hash_object.update(password.text.encode("utf-8"))

        return PasswordHash(hash_object.hexdigest())
