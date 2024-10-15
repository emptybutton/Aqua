from dataclasses import dataclass
from hashlib import sha256
from string import digits


@dataclass(kw_only=True, frozen=True, slots=True)
class Password:
    class Error(Exception): ...

    class WeekError(Error): ...

    class TooShortError(WeekError): ...

    class OnlySmallLettersError(WeekError): ...

    class OnlyCapitalLettersError(WeekError): ...

    class OnlyDigitsError(WeekError): ...

    class NoDigitsError(WeekError): ...

    text: str

    def __post_init__(self) -> None:
        if len(self.text) < 8:
            raise Password.TooShortError

        if self.__has_no_digits():
            raise Password.NoDigitsError

        if self.__has_only_digits():
            raise Password.OnlyDigitsError

        if self.text.upper() == self.text:
            raise Password.OnlyCapitalLettersError

        if self.text.lower() == self.text:
            raise Password.OnlySmallLettersError

    def __has_no_digits(self) -> bool:
        return set(digits) - set(self.text) == set(digits)

    def __has_only_digits(self) -> bool:
        return set(self.text) - set(digits) == set()


@dataclass(kw_only=True, frozen=True, slots=True)
class PasswordHash:
    class Error(Exception): ...

    class EmptyError(Error): ...

    text: str

    def __post_init__(self) -> None:
        if len(self.text) == 0:
            raise PasswordHash.EmptyError


def hash_of(password: Password) -> PasswordHash:
    hash_ = sha256()
    hash_.update(password.text.encode("utf-8"))

    return PasswordHash(text=hash_.hexdigest())
