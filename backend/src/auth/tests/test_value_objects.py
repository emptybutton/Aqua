from src.auth.domain.value_objects import Password, PasswordHash


def test_hashing() -> None:
    pasword_a = Password("123abcABC")
    pasword_b = Password("123abcABC")
    pasword_c = Password("123ABCabc")

    password_hash = PasswordHash.of(pasword_a)
    assert password_hash == password_hash  # noqa: PLR0124

    assert PasswordHash.of(pasword_a) == PasswordHash.of(pasword_a)
    assert PasswordHash.of(pasword_a) == PasswordHash.of(pasword_b)
    assert PasswordHash.of(pasword_a) != PasswordHash.of(pasword_c)
    assert PasswordHash.of(pasword_b) != PasswordHash.of(pasword_c)
