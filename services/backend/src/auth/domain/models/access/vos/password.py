from dataclasses import dataclass
from hashlib import sha256
from string import digits
from typing import Literal

from result import Err, Ok, Result

from auth.domain.framework.safe import SafeImmutable


@dataclass(kw_only=True, frozen=True, slots=True)
class Password(SafeImmutable):
    text: str

    @classmethod
    def with_(
        cls, *, text: str
    ) -> Result[
        "Password",
        Literal[
            "password_too_short",
            "password_contains_only_small_letters",
            "password_contains_only_capital_letters",
            "password_contains_only_digits",
            "password_has_no_numbers",
        ],
    ]:
        password = cls(text=text, is_safe=True)

        if len(password.text) < 8:
            return Err("password_too_short")

        if _has_no_digits(password):
            return Err("password_has_no_numbers")

        if _has_only_digits(password):
            return Err("password_contains_only_digits")

        if password.text.upper() == password.text:
            return Err("password_contains_only_capital_letters")

        if password.text.lower() == password.text:
            return Err("password_contains_only_small_letters")

        return Ok(password)


def _has_no_digits(password: Password) -> bool:
    return set(digits) - set(password.text) == set(digits)


def _has_only_digits(password: Password) -> bool:
    return set(password.text) - set(digits) == set()


@dataclass(kw_only=True, frozen=True, slots=True)
class PasswordHash:
    text: str


def hash_of(password: Password) -> PasswordHash:
    hash_ = sha256()
    hash_.update(password.text.encode("utf-8"))

    return PasswordHash(text=hash_.hexdigest())
