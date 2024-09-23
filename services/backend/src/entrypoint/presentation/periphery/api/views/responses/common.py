from collections import defaultdict
from typing import Any, Callable, Generic, Mapping, TypeAlias, TypeVar, Union

from fastapi import BackgroundTasks, status
from fastapi.responses import Response
from pydantic import BaseModel


_BaseModelT_co = TypeVar("_BaseModelT_co", bound=BaseModel, covariant=True)

_Doc: TypeAlias = dict[int | str, dict[str, Any]]


class View(Generic[_BaseModelT_co]):
    def __init__(
        self,
        body_type: type[_BaseModelT_co],
        status_code: int = status.HTTP_200_OK,
        extended: Callable[[Response], Response] = lambda v: v,
    ) -> None:
        self.__body_type = body_type
        self.__status_code = status_code
        self.__extended = extended

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
        background: BackgroundTasks | None = None,
    ) -> Response:
        model = self.__body_type() if model is None else model
        response = Response(
            model.model_dump_json(),
            self.__status_code,
            headers,
            "application/json",
            background,
        )

        return self.__extended(response)


def to_doc(*views: View[BaseModel]) -> _Doc:
    body_types_by_status_code: dict[int, list[type[BaseModel]]]
    body_types_by_status_code = defaultdict(list)

    for view in views:
        body_types_by_status_code[view.status_code].append(view.body_type)

    return {
        status_code: {
            "model": (
                body_types[0] if len(body_types) == 1 else Union[*body_types]
            )
        }
        for status_code, body_types in body_types_by_status_code.items()
    }
