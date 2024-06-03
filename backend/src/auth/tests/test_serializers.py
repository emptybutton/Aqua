from datetime import datetime

from src.auth.domain.value_objects import Password, AccessToken, Username
from src.auth.infrastructure.adapters import serializers


def test_password_serializer() -> None:
    pasword_a = Password("123abcABC")
    pasword_b = Password("123abcABC")
    pasword_c = Password("123ABCabc")

    serializer = serializers.PasswordSerializer()

    password_hash = serializer.serialized(pasword_a)
    assert password_hash == password_hash  # noqa: PLR0124

    assert serializer.serialized(pasword_a) == serializer.serialized(pasword_a)
    assert serializer.serialized(pasword_a) == serializer.serialized(pasword_b)
    assert serializer.serialized(pasword_a) != serializer.serialized(pasword_c)
    assert serializer.serialized(pasword_b) != serializer.serialized(pasword_c)

    long_pasword = Password("a" * 32 + "B" * 32 + "44" * 32)
    serializer.serialized(long_pasword)


def test_access_token_serializer() -> None:
    serializer = serializers.AccessTokenSerializer("megasecret")

    access_token = AccessToken(
        None,
        Username("Igor"),
        datetime.fromtimestamp(0),
    )

    jwt = serializer.serialized(access_token)

    assert serializer.deserialized(jwt) == access_token
