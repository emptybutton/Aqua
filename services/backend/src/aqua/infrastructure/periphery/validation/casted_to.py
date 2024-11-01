from typing import Any

from aqua.infrastructure.periphery.validation.error import ValidationError


def casted_to[ValueT](type_: type[ValueT], value: Any) -> ValueT:  # noqa: ANN401
    if isinstance(value, type_):
        return value

    raise ValidationError
