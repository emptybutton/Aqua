from typing import Mapping, TypeVar, Callable, Generic, Any, TypeAlias

from fastapi import BackgroundTasks, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


_BaseModelT_co = TypeVar(
    "_BaseModelT_co",
    bound=BaseModel,
    covariant=True,
)

_Doc: TypeAlias = dict[int | str, dict[str, Any]]


class View(Generic[_BaseModelT_co]):
    def __init__(
        self,
        body_type: type[_BaseModelT_co],
        status_code: int = status.HTTP_200_OK,
    ) -> None:
        self.__body_type = body_type
        self.__status_code = status_code

    @property
    def body_type(self) -> type[_BaseModelT_co]:
        return self.__body_type

    @property
    def status_code(self) -> int:
        return self.__status_code

    def to_doc(
        self,
        get_other: Callable[[type[_BaseModelT_co]], dict[str, Any]] = (
            lambda _: dict()
        ),
    ) -> _Doc:
        return {
            self.__status_code: {
                "model": self.__body_type,
                **get_other(self.__body_type),
            }
        }

    def to_response(
        self,
        model: _BaseModelT_co | None = None,
        *,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTasks | None = None,
    ) -> JSONResponse:
        return JSONResponse(
            self.__body_type() if model is None else model.model_dump(),
            self.__status_code,
            headers,
            media_type,
            background,
        )


def to_doc(*views: View[BaseModel]) -> _Doc:
    return {
        view.status_code: {"model": view.body_type}
        for view in views
    }
