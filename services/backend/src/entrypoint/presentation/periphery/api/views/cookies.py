from datetime import datetime, UTC
from uuid import UUID

from fastapi import Response


class SessionCookie:
    def __init__(self, response: Response) -> None:
        self.__response = response

    def set(self, session_id: UUID, expiration_date: datetime) -> None:
        expiration_timedelta = expiration_date - datetime.now(UTC)

        self.__response.set_cookie(
            "session_id",
            str(session_id),
            httponly=True,
            expires=expiration_timedelta.seconds,
        )

        self.__response.set_cookie(
            "session_expiration_date",
            str(expiration_date.timestamp()),
            httponly=True,
            expires=expiration_timedelta.seconds,
        )

    def delete(self) -> None:
        self.__response.delete_cookie("session_id", httponly=True)
        self.__response.delete_cookie("session_expiration_date", httponly=True)
