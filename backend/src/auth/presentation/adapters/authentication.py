from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from secrets import token_hex

from src.auth.application import authentication
from src.auth.infrastructure.adapters import serializers
from src.auth.presentation import secrets


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    new_refresh_token_text: str
    new_refresh_token_expiration_date: datetime
    serialized_new_access_token: str


def authenticate_user(
    serialized_access_token: str,
    refresh_token_text: str,
    refresh_token_expiration_date: datetime,
) -> Optional[OutputDTO]:
    serializer = serializers.AccessTokenSerializer(secrets.jwt_secret)

    result = authentication.authenticate_user(
        serialized_access_token,
        refresh_token_text,
        refresh_token_expiration_date,
        access_token_serializer=serializer,
        generate_refresh_token_text=token_hex,
    )

    if result is None:
        return None

    expiration_date = result.new_refresh_token.expiration_date

    return OutputDTO(
        new_refresh_token_text=result.new_refresh_token.text,
        new_refresh_token_expiration_date=expiration_date,
        serialized_new_access_token=result.serialized_new_access_token,
    )
