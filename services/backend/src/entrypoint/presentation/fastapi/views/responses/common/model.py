from collections import defaultdict
from typing import Any, Callable, Mapping, Union

from fastapi import BackgroundTasks, status
from fastapi.responses import Response
from pydantic import BaseModel


type _Doc = dict[int | str, dict[str, Any]]


class ResponseModel[BaseModelT: BaseModel]:
    def __init__(
        self,
        body_type: type[BaseModelT],
        status_code: int = status.HTTP_200_OK,
        extended: Callable[[Response], Response] = lambda v: v,
    ) -> None:
        self.__body_type = body_type
        self.__status_code = status_code
        self.__extended = extended

    @property
    def body_type(self) -> type[BaseModelT]:
        return self.__body_type

    @property
    def status_code(self) -> int:
        return self.__status_code

    def to_response(
        self,
        model: BaseModelT | None = None,
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


def to_doc(*response_models: ResponseModel[BaseModel]) -> _Doc:
    body_types_by_status_code: dict[int, list[type[BaseModel]]]
    body_types_by_status_code = defaultdict(list)

    for response_model in response_models:
        body_types = body_types_by_status_code[response_model.status_code]
        body_types.append(response_model.body_type)

    return {
        status_code: {
            "model": (
                body_types[0] if len(body_types) == 1 else Union[*body_types]
            )
        }
        for status_code, body_types in body_types_by_status_code.items()
    }
