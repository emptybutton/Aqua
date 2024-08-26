from pytest import raises

from auth.domain import value_objects as vos


def test_creation_with_empty_text() -> None:
    with raises(vos.Username.EmptyError):
        vos.Username(text="")
