from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyCookie

from entrypoint.presentation.fastapi.views import cookies


_session_cookie_scheme = APIKeyCookie(
    name=cookies.SessionCookie.name,
    scheme_name="Session id cookie",
    description="Scheme for authentication via web sessions.",
)
type session_id_cookie = Annotated[str, Depends(_session_cookie_scheme)]


_optional_session_cookie_scheme = APIKeyCookie(
    name=cookies.SessionCookie.name,
    scheme_name="Optional session id cookie",
    description="Scheme for possible authentication via web sessions.",
    auto_error=False,
)
type optional_session_id_cookie = Annotated[
    str | None, Depends(_optional_session_cookie_scheme)
]
