from pytest import raises

from aqua.domain.framework.safe import (
    SafeImmutable,
    SafeMutable,
    UnsafeValueError,
)


def test_safe_immutable_unsafe_creation() -> None:
    with raises(UnsafeValueError):
        SafeImmutable(is_safe=False)


def test_safe_mutable_unsafe_creation() -> None:
    with raises(UnsafeValueError):
        SafeMutable(is_safe=False)


def test_safe_immutable_safe_creation() -> None:
    SafeImmutable(is_safe=True)


def test_safe_mutable_safe_creation() -> None:
    SafeMutable(is_safe=True)
