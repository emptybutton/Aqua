from pytest import raises

from auth.domain import value_objects as vos


def test_valid_password() -> None:
    password = vos.Password(text="Ab345678")

    assert isinstance(password, vos.Password)


def test_too_short_password() -> None:
    with raises(vos.Password.TooShortError):
        vos.Password(text="Ab34567")


def test_password_with_only_small_letters() -> None:
    with raises(vos.Password.OnlySmallLettersError):
        vos.Password(text="ab345678")


def test_password_with_only_capital_letters() -> None:
    with raises(vos.Password.OnlyCapitalLettersError):
        vos.Password(text="AB345678")


def test_password_with_only_digits() -> None:
    with raises(vos.Password.OnlyDigitsError):
        vos.Password(text="12345678")


def test_password_with_no_digits_error() -> None:
    with raises(vos.Password.NoDigitsError):
        vos.Password(text="Abcdefgh")
