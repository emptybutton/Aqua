from datetime import datetime, UTC
from typing import Optional

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


def refresh_token_expiration_date_from(
    timestamp_line: str,
) -> Optional[datetime]:
    try:
        timestamp = float(timestamp_line)
    except ValueError:
        return None

    return datetime.fromtimestamp(timestamp, UTC)
