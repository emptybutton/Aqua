from typing import Annotated, TypeAlias

from fastapi import Depends
from fastapi.security import APIKeyCookie

from entrypoint.presentation.fastapi.views import cookies


session_cookie_scheme = APIKeyCookie(
    name=cookies.SessionCookie.name,
    scheme_name="Session id cookie",
    description="Scheme for authentication via web sessions.",
)
session_id_cookie: TypeAlias = Annotated[str, Depends(session_cookie_scheme)]


optional_session_cookie_scheme = APIKeyCookie(
    name=cookies.SessionCookie.name,
    scheme_name="Optional session id cookie",
    description="Scheme for possible authentication via web sessions.",
    auto_error=False,
)
optional_session_id_cookie: TypeAlias = Annotated[
    str | None, Depends(optional_session_cookie_scheme)
]
