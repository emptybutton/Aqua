from src.auth.domain.value_objects import Password
from src.auth.infrastructure.serializers import PasswordSerializer


def test_password_hashing() -> None:
    pasword_a = Password("123abcABC")
    pasword_b = Password("123abcABC")
    pasword_c = Password("123ABCabc")

    serializer = PasswordSerializer()

    password_hash = serializer.serialized(pasword_a)
    assert password_hash == password_hash  # noqa: PLR0124

    assert serializer.serialized(pasword_a) == serializer.serialized(pasword_a)
    assert serializer.serialized(pasword_a) == serializer.serialized(pasword_b)
    assert serializer.serialized(pasword_a) != serializer.serialized(pasword_c)
    assert serializer.serialized(pasword_b) != serializer.serialized(pasword_c)

    long_pasword = Password("a" * 32 + "B" * 32 + "44" * 32)
    serializer.serialized(long_pasword)
