from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class SafeImmutable:
    safe: bool = False

    def __post_init__(self) -> None:
        _validate(self)


@dataclass(kw_only=True)
class SafeMutable:
    safe: bool = False

    def __post_init__(self) -> None:
        _validate(self)


type Safe = SafeImmutable | SafeMutable


def _validate(value: Safe) -> None:
    msg = (
        "create in safe ways: using other constructors or"
        "specifying `safe=True`."
    )
    assert value.safe, msg  # noqa: S101
