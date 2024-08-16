from datetime import datetime, UTC

from fastapi import Response


class RefreshTokenCookie:
    def __init__(self, response: Response) -> None:
        self.__response = response

    def set(self, refresh_token: str, expiration_date: datetime) -> None:
        expiration_timedelta = expiration_date - datetime.now(UTC)

        self.__response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            expires=expiration_timedelta.seconds,
        )

        self.__response.set_cookie(
            "refresh_token_expiration_date",
            str(expiration_date.timestamp()),
            httponly=True,
            expires=expiration_timedelta.seconds,
        )

    def delete(self) -> None:
        self.__response.delete_cookie("refresh_token", httponly=True)
        self.__response.delete_cookie(
            "refresh_token_expiration_date",
            httponly=True,
        )


class JWTCookie:
    def __init__(self, response: Response) -> None:
        self.__response = response

    def set(self, jwt: str) -> None:
        self.__response.set_cookie("jwt", jwt, httponly=True)

    def delete(self) -> None:
        self.__response.delete_cookie("jwt", httponly=True)


class RottenJWTCookie:
    def __init__(self, response: Response) -> None:
        self.__response = response

    def set(self, jwt: str) -> None:
        self.__response.set_cookie("rotten_jwt", jwt, httponly=True)

    def delete(self) -> None:
        self.__response.delete_cookie("rotten_jwt", httponly=True)
