from typing import Any


class SerializingError(Exception): ...


class StrictSerializingObject:
    def __init__(self, value: dict[str, Any]) -> None:
        self.__value = value

    def __getitem__[ValueT](
        self, field_data: tuple[str | list[str], type[ValueT]]
    ) -> ValueT:
        field_names, field_type = field_data

        if isinstance(field_names, str):
            field_names = (field_names, )

        for field_name in field_names:
            value = self.__value.get(field_name)

            if isinstance(value, field_type):
                return value

        raise SerializingError


def casted_to[ValueT](type_: type[ValueT], value: Any) -> ValueT:  # noqa: ANN401
    if isinstance(value, type_):
        return value

    raise SerializingError
