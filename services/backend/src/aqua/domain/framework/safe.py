from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True)
class SafeImmutable:
    is_safe: bool = field(repr=False)

    def __post_init__(self) -> None:
        _validate(self)


@dataclass(kw_only=True)
class SafeMutable:
    is_safe: bool = field(repr=False)

    def __post_init__(self) -> None:
        _validate(self)


type Safe = SafeImmutable | SafeMutable


class UnsafeValueError(Exception): ...


def _validate(value: Safe) -> None:
    msg = (
        "create in safe ways: using other constructors or"
        " specifying `is_safe=True`."
    )
    if not value.is_safe:
        raise UnsafeValueError(msg)
