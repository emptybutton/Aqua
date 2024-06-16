from functools import reduce
from typing import TypeAlias, TypedDict
from operator import add

from fastapi import HTTPException, status

from src.aqua.presentation import errors as aqua_errors
from src.auth.presentation import errors as auth_errors


class _DetailBody(TypedDict):
    msg: str
    type: str


Detail: TypeAlias = list[_DetailBody]


def detail_from(type_: str, message: str) -> Detail:
    return [
        {
            "msg": message,
            "type": type_,
        }
    ]


def detail_of(error: Exception, *, message: str = str()) -> Detail:  # noqa: UP018
    return detail_from(detail_type_of(error), message)


def detail_type_of(error: Exception) -> str:
    raw_type = type(error).__name__
    has_error_prefix = raw_type.lower().endswith("error")

    return raw_type if has_error_prefix else f"{raw_type}Error"


def combined(*details: Detail) -> Detail:
    return reduce(add, details)


def default_error_with(detail: Detail) -> HTTPException:
    return HTTPException(status.HTTP_400_BAD_REQUEST, detail=detail)


def for_api(error: Exception) -> Exception:
    default_detail = detail_of(error)
    default_error = default_error_with(default_detail)

    if isinstance(error, auth_errors.WeekPassword):
        message = (
            "password must not contain only numbers or only letters, "
            "but must contain both upper and lower case letters and be 8 "
            "or more characters long"
        )

        return HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=detail_of(error, message=message),
        )

    if isinstance(
        error,
        aqua_errors.ValidationError | auth_errors.ValidationError,
    ):
        return default_error

    return error