from functools import partial
from secrets import token_hex

from pytest import raises, mark

from src.auth.application import cases, errors as application_errors
from src.auth.application.ports.places import Place  # noqa: TCH001
from src.auth.domain import value_objects, errors as domain_errors
from src.auth.infrastructure import serializers
from src.auth.tests import adapters
from src.shared.infrastructure import uows


@mark.asyncio
async def test_register_user() -> None:
    users = adapters.Users()
    access_token_serializer = serializers.AccessTokenSerializer("megasecret")

    register_user = partial(
        cases.register_user,
        users=users,
        uow_for=lambda _: uows.UoW(),
        password_serializer=serializers.PasswordSerializer(),
        generate_refresh_token_text=token_hex,
        access_token_serializer=access_token_serializer,
    )

    refresh_token_place: Place[value_objects.RefreshToken] = adapters.Place()

    with raises(domain_errors.WeekPassword):
        await register_user("Igor", "1234", refresh_token_place)

    assert refresh_token_place.get() is None
    assert len(users.storage) == 0

    dto = await register_user("Igor", "123ABCabc", refresh_token_place)

    assert len(users.storage) == 1

    assert dto.refresh_token == refresh_token_place.get()
    assert not dto.refresh_token.is_expired

    access_token = access_token_serializer.deserialized(
        dto.serialized_access_token,
    )
    assert access_token is not None, dto.serialized_access_token
    assert access_token.username.text == "Igor"
    assert not access_token.is_expired

    with raises(application_errors.UserIsAlreadyRegistered):
        await register_user("Igor", "123ABCabc", refresh_token_place)

    assert len(users.storage) == 1

    await register_user("Oleg", "123ABCabc", refresh_token_place)

    assert len(users.storage) == 2  # noqa: PLR2004
    assert dto.refresh_token != refresh_token_place.get()
