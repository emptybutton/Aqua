from functools import cached_property
from typing import Any

from aqua.infrastructure.periphery.validation.error import ValidationError


type _RawParams[V] = tuple[str | list[str], type[V]]
type _Params[V] = tuple[list[str], type[V]]


class _ValidationObject:
    def __init__(self, value: dict[str, Any]) -> None:
        self.__value = value

    def _params_of[V](self, raw_params: _RawParams[V]) -> _Params[V]:
        field_name_value, field_type = raw_params

        if isinstance(field_name_value, str):
            field_names = [field_name_value]
        else:
            field_names = field_name_value

        return field_names, field_type


class NotStrictValidationObject(_ValidationObject):
    @cached_property
    def y(self) -> "StrictValidationObject":
        return StrictValidationObject(self.__value)

    def __getitem__[V](self, raw_params: _RawParams[V]) -> V | None:
        field_names, field_type = self._params_of(raw_params)

        for field_name in field_names:
            value = self.__value.get(field_name)

            if isinstance(value, field_type):
                return value

        return None


class StrictValidationObject(_ValidationObject):
    @cached_property
    def n(self) -> "NotStrictValidationObject":
        return NotStrictValidationObject(self.__value)

    def __getitem__[V](self, raw_params: _RawParams[V]) -> V:
        field_names, field_type = self._params_of(raw_params)

        for field_name in field_names:
            value = self.__value.get(field_name)

            if isinstance(value, field_type):
                return value

        raise ValidationError
