from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from auth.domain.value_objects import PasswordHash, SessionLifetime, Username


@dataclass(kw_only=True)
class PreviousUsername:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    username: Username
    change_time: datetime | None

    class Error(Exception): ...

    class NotUTCChangeTimeError(Error): ...

    def __post_init__(self) -> None:
        if self.change_time is not None and self.change_time.tzinfo is not UTC:
            raise PreviousUsername.NotUTCChangeTimeError


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
        current_time: datetime | None = None,
    ) -> "Session":
        if self.password_hash != password_hash:
            raise User.IncorrectPasswordHashForAuthorizationError

        return Session.for_(self, start_time=current_time)

    def change_name(
        self,
        *,
        new_username: Username,
        current_time: datetime | None,
    ) -> PreviousUsername:
        previous_username = PreviousUsername(
            username=self.name, user_id=self.id, change_time=current_time,
        )
        self.name = new_username

        return previous_username

    @classmethod
    def register(
        cls,
        name: Username,
        password_hash: PasswordHash,
        *,
        current_time: datetime | None = None,
    ) -> tuple["User", "Session"]:
        user = User(name=name, password_hash=password_hash)
        session = Session.for_(user, start_time=current_time)

        return user, session


@dataclass(kw_only=True)
class Session:
    class Error(Exception): ...

    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    lifetime: SessionLifetime

    class AuthenticationError(Error): ...

    class ExpiredLifetimeForAuthenticationError(AuthenticationError): ...

    def authenticate(self, *, time_point: datetime | None = None) -> None:
        if time_point is None:
            time_point = datetime.now(UTC)

        if self.lifetime.expired(time_point=time_point):
            raise Session.ExpiredLifetimeForAuthenticationError

        self.lifetime = self.lifetime.extend(time_point=time_point)

    @classmethod
    def for_(
        cls, user: User, *, start_time: datetime | None = None
    ) -> "Session":
        if start_time is None:
            start_time = datetime.now(UTC)

        lifetime = SessionLifetime(_start_time=start_time)

        return Session(user_id=user.id, lifetime=lifetime)
