from typing import Annotated, TypeAlias
from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyCookie

from entrypoint.presentation.periphery.api.views import cookies


_session_cookie_scheme = APIKeyCookie(
    name=cookies.SessionCookie.name,
    scheme_name="Session id cookie",
    description="Scheme for authentication via web sessions.",
)
session_id_cookie: TypeAlias = Annotated[UUID, Depends(_session_cookie_scheme)]


_optional_session_cookie_scheme = APIKeyCookie(
    name=cookies.SessionCookie.name,
    scheme_name="Optional session id cookie",
    description="Scheme for possible authentication via web sessions.",
    auto_error=False,
)
optional_session_id_cookie: TypeAlias = Annotated[
    UUID | None, Depends(_optional_session_cookie_scheme)
]
