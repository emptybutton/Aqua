from functools import partial
from secrets import token_hex

from pytest import raises, mark

from auth.application.cases import registration
from auth.domain import errors as domain_errors
from auth.infrastructure.adapters import serializers
from auth.tests import adapters
from shared.infrastructure.adapters import uows


@mark.asyncio
async def test_register_user() -> None:
    users = adapters.Users()
    access_token_serializer = serializers.AccessTokenSerializer("megasecret")

    register_user = partial(
        registration.register_user,
        users=users,
        uow_for=lambda _: uows.FakeUoW(),
        password_serializer=serializers.PasswordSerializer(),
        generate_refresh_token_text=token_hex,
        access_token_serializer=access_token_serializer,
    )

    with raises(domain_errors.WeekPassword):
        await register_user("Igor", "1234")

    assert len(users.storage) == 0

    result = await register_user("Igor", "123ABCabc")

    assert len(users.storage) == 1

    assert not result.refresh_token.is_expired

    access_token = access_token_serializer.deserialized(
        result.serialized_access_token,
    )
    assert access_token is not None, result.serialized_access_token
    assert access_token.username.text == "Igor"
    assert not access_token.is_expired

    with raises(registration.UserIsAlreadyRegisteredError):
        await register_user("Igor", "123ABCabc")

    assert len(users.storage) == 1

    await register_user("Oleg", "123ABCabc")

    assert len(users.storage) == 2  # noqa: PLR2004
