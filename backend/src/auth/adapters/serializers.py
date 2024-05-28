from typing import TypeAlias, Optional

import jwt

from src.auth.domain.value_objects import AccessToken
from src.auth.application.ports.serializers import Serializer


JWT: TypeAlias = str


class AccessTokenSerializer(Serializer[AccessToken, JWT]):
    def __init__(self, secret: str) -> None:
        self.__secret = secret

    def serialize(self, access_token: AccessToken) -> JWT:
        payload = {
            "user-id": access_token.user_id,
            "username": access_token.username.text,
        }

        headers = {
            "exp": access_token.expiration_date.timestamp(),
        }

        return jwt.encode(payload, self.__secret, headers=headers)

    def deserialize(
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
