from datetime import datetime, UTC
from typing import TypeAlias
from uuid import UUID
import hashlib

import jwt

from auth.application.ports import serializers
from auth.domain import value_objects as vos


JWT: TypeAlias = str


class AccessTokenSerializer(
    serializers.SecureSymmetricSerializer[vos.AccessToken, JWT],
):
    def __init__(self, secret: str, *, algorithm: str = "HS256") -> None:
        self.__secret = secret
        self.__algorithm = algorithm

    def serialized(self, access_token: vos.AccessToken) -> JWT:
        payload = {
            "user-id": int(access_token.user_id),
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

    def deserialized(self, jwt_: JWT) -> vos.AccessToken | None:
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
            return vos.AccessToken(
                user_id=user_id,
                expiration_date=expiration_date,
            )
        except vos.AccessToken.Error:
            return None


class PasswordSerializer(
    serializers.AsymmetricSerializer[vos.Password, vos.PasswordHash],
):
    def serialized(self, password: vos.Password) -> vos.PasswordHash:
        hash_object = hashlib.sha256()
        hash_object.update(password.text.encode("utf-8"))

        return vos.PasswordHash(text=hash_object.hexdigest())
