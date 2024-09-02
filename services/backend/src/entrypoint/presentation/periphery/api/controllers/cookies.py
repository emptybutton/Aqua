from typing import Annotated, TypeAlias
from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyCookie

from entrypoint.presentation.periphery.api.views import cookies


_scheme_description = (
    "Scheme for authentication via web sessions."
    " This is the only way to authenticate"
)
_session_cookie_scheme = APIKeyCookie(
    name=cookies.SessionCookie.name,
    scheme_name="Session id cookie",
    description=_scheme_description,
)
session_id_cookie: TypeAlias = Annotated[UUID, Depends(_session_cookie_scheme)]
