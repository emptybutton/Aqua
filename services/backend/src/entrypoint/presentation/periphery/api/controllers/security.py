from fastapi.security import APIKeyCookie


jwt_cookie_scheme = APIKeyCookie(name="jwt")
