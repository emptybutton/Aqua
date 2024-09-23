from dataclasses import dataclass, field
from uuid import UUID, uuid4

from auth.domain.value_objects import (
    PasswordHash,
    SessionLifetime,
    Time,
    Username,
)


@dataclass(kw_only=True)
class PreviousUsername:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    username: Username
    change_time: Time | None


@dataclass(kw_only=True)
class User:
    class Error(Exception): ...

    id: UUID = field(default_factory=uuid4)
    name: Username
    password_hash: PasswordHash

    class AuthorizationError(Error): ...

    class IncorrectPasswordHashForAuthorizationError(AuthorizationError): ...

    def authorize(
        self,
        *,
        password_hash: PasswordHash,
        current_time: Time,
    ) -> "Session":
        if self.password_hash != password_hash:
            raise User.IncorrectPasswordHashForAuthorizationError

        return Session.for_(self, current_time=current_time)

    def change_name(
        self,
        *,
        new_username: Username,
        current_time: Time,
    ) -> PreviousUsername:
        previous_username = PreviousUsername(
            username=self.name,
            user_id=self.id,
            change_time=current_time,
        )
        self.name = new_username

        return previous_username

    class PasswordChangeError(Error): ...

    class OtherUserSessionForPasswordChangeError(PasswordChangeError): ...

    def change_password(
        self,
        *,
        new_password_hash: PasswordHash,
        other_sessions: tuple["Session", ...],
    ) -> None:
        for other_session in other_sessions:
            if other_session.user_id != self.id:
                raise User.OtherUserSessionForPasswordChangeError

        self.password_hash = new_password_hash

        for other_session in other_sessions:
            other_session.cancel()

    @classmethod
    def register(
        cls,
        name: Username,
        password_hash: PasswordHash,
        *,
        current_time: Time,
    ) -> tuple["User", "Session"]:
        user = User(name=name, password_hash=password_hash)
        session = Session.for_(user, current_time=current_time)

        return user, session


@dataclass(kw_only=True)
class Session:
    class Error(Exception): ...

    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    lifetime: SessionLifetime
    cancelled: bool = False

    def cancel(self) -> None:
        self.cancelled = True

    class AuthenticationError(Error): ...

    class ExpiredLifetimeForAuthenticationError(AuthenticationError): ...

    class CancelledForAuthenticationError(AuthenticationError): ...

    def authenticate(self, *, current_time: Time) -> None:
        if self.lifetime.expired(current_time=current_time):
            raise Session.ExpiredLifetimeForAuthenticationError

        if self.cancelled:
            raise Session.CancelledForAuthenticationError

        self.lifetime = self.lifetime.extend(current_time=current_time)

    @classmethod
    def for_(cls, user: User, *, current_time: Time) -> "Session":
        lifetime = SessionLifetime(start_time=current_time)

        return Session(user_id=user.id, lifetime=lifetime)
