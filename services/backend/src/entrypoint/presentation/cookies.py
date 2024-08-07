from datetime import datetime, UTC

from fastapi import Response


def set_refresh_token(
    response: Response,
    refresh_token: str,
    expiration_date: datetime,
) -> None:
    expiration_timedelta = datetime.now(UTC) - expiration_date

    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        expires=expiration_timedelta.seconds,
    )

    response.set_cookie(
        "refresh_token_expiration_date",
        str(expiration_date.timestamp),
        httponly=True,
        expires=expiration_timedelta.seconds,
    )
