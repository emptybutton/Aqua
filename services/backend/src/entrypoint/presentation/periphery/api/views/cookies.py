from uuid import UUID

from fastapi import Response


class SessionCookie:
    def __init__(self, response: Response) -> None:
        self.__response = response

    def set(self, session_id: UUID) -> None:
        self.__response.set_cookie(
            "session_id",
            str(session_id),
            httponly=True,
        )

    def delete(self) -> None:
        self.__response.delete_cookie("session_id", httponly=True)
