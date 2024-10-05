from dataclasses import dataclass
from typing import Iterable, TypeAlias
from uuid import UUID, uuid4

from auth.domain.models.access.aggregates.account.internal import (
    account_name as _account_name,
)
from auth.domain.models.access.aggregates.account.internal import (
    session as _session,
)
from auth.domain.models.access.pure.vos import password as _password
from auth.domain.models.access.pure.vos import time as _time
from shared.domain.framework.pure import entity as _entity
from shared.domain.framework.pure.ports.effect import Effect


@dataclass(kw_only=True, frozen=True, slots=True)
class PasswordChange(_entity.MutationEvent["Account"]):
    new_password_hash: _password.PasswordHash


AccountEvent: TypeAlias = PasswordChange


@dataclass(kw_only=True, eq=False)
class Account(_entity.Entity[UUID, AccountEvent]):
    class Error(Exception): ...

    current_name: _account_name.AccountName
    previous_names: set[_account_name.AccountName]
    sessions: set[_session.Session]
    password_hash: _password.PasswordHash

    class PrimaryAuthenticationError(Error): ...

    class InvalidPasswordHashForPrimaryAuthenticationError(Error): ...

    def primary_authenticate(self, *, password: _password.Password) -> None:
        password_hash = _password.hash_of(password)

        if self.password_hash != password_hash:
            raise Account.InvalidPasswordHashForPrimaryAuthenticationError

    class SecondaryAuthenticationError(Error): ...

    class NoSessionError(SecondaryAuthenticationError): ...

    class ExpiredForSecondaryAuthenticationError(SecondaryAuthenticationError):
        ...

    class CancelledForSecondaryAuthenticationError(
        SecondaryAuthenticationError
    ): ...

    class ReplacedForSecondaryAuthenticationError(SecondaryAuthenticationError):
        ...

    def secondarily_authenticate(
        self, *, session_id: UUID, current_time: _time.Time, effect: Effect,
    ) -> _session.Session:
        session = self.__session_with(session_id)

        if not session:
            raise Account.NoSessionError

        reasons = session.inactivity_reasons_when(current_time=current_time)

        if "replaced" in reasons:
            raise Account.ReplacedForAuthenticationError

        if "expired" in reasons:
            raise Account.ExpiredForAuthenticationError

        if "cancelled" in reasons:
            raise Account.CancelledForAuthenticationError

        _session.extend(session, current_time=current_time, effect=effect)
        return session

    @dataclass(kw_only=True, frozen=True, slots=True)
    class NameChangeOutput:
        previous_name: _account_name.AccountName | None

    def change_name(
        self,
        *,
        new_name_text: str,
        current_time: _time.Time,
        effect: Effect,
    ) -> NameChangeOutput:
        if new_name_text == self.current_name.text:
            return Account.NameChangeOutput(previous_name=None)

        previous_current_name = self.current_name
        previous_name = self.__previous_name_with(text=new_name_text)
        output = Account.NameChangeOutput(previous_name=previous_current_name)

        if previous_name:
            self.__make_previous_name_current(
                previous_name,
                current_time=current_time,
                effect=effect,
            )
            return output

        self.__make_current_name_previous(effect=effect)
        self.current_name = _account_name.AccountName.create(
            text=new_name_text,
            current_time=current_time,
            account_id=self.id,
            effect=effect,
        )
        return output

    class PasswordChangeError(Error): ...

    class NoSessionForPasswordChangeError(PasswordChangeError): ...

    def change_password(
        self,
        *,
        new_password: _password.Password,
        current_session_id: UUID,
        effect: Effect,
    ) -> None:
        current_session = self.__session_with(current_session_id)

        if current_session is None:
            raise Account.NoSessionForPasswordChangeError

        new_password_hash = _password.hash_of(new_password)

        if self.password_hash == new_password_hash:
            return

        self.password_hash = new_password_hash

        event = PasswordChange(entity=self, new_password_hash=new_password_hash)
        self.events.append(event)
        effect.consider(self)

        other_sessions = (
            self.__other_sessions_when(current_session=current_session)
        )
        for other_session in other_sessions:
            _session.cancel(other_session, effect=effect)

    @dataclass(kw_only=True, frozen=True, slots=True)
    class CreationOutput:
        account: "Account"
        current_session: _session.Session

    @classmethod
    def create(
        cls,
        *,
        name_text: str,
        password: _password.Password,
        effect: Effect,
        current_time: _time.Time,
        current_session: _session.Session | None = None,
    ) -> CreationOutput:
        account_id = uuid4()
        name = _account_name.AccountName.create(
            text=name_text,
            current_time=current_time,
            account_id=account_id,
            effect=effect,
        )
        password_hash = _password.hash_of(password)

        current_session = _session.issue_session(
            account_id=account_id,
            current_time=current_time,
            current_session=current_session,
            effect=effect,
        )

        account = Account(
            id=account_id,
            current_name=name,
            previous_names=set(),
            sessions={current_session},
            password_hash=password_hash,
            events=[_entity.Created(entity_id=account_id)],
        )
        effect.consider(account)

        return Account.CreationOutput(
            account=account, current_session=current_session
        )

    def __session_with(self, session_id: UUID) -> _session.Session | None:
        for session in self.sessions:
            if session.id == session_id:
                return session

        return None

    def __other_sessions_when(
        self, *, current_session: _session.Session
    ) -> Iterable[_session.Session]:
        return (session != current_session for session in self.sessions)

    def __previous_name_with(
        self, *, text: str
    ) -> _account_name.AccountName | None:
        for previous_name in self.previous_names:
            if text == previous_name.text:
                return previous_name

        return None

    def __make_current_name_previous(
        self,
        *,
        effect: Effect,
    ) -> None:
        self.current_name.become_previous(effect=effect)
        self.previous_names.add(self.current_name)

    def __make_previous_name_current(
        self,
        previous_name: _account_name.AccountName,
        *,
        current_time: _time.Time,
        effect: Effect,
    ) -> None:
        self.__make_current_name_previous(effect=effect)

        previous_name.become_current(
            current_time=current_time, effect=effect
        )
        self.current_name = previous_name
        self.previous_names.remove(self.current_name)


def login_to(
    account: Account,
    *,
    password: _password.Password,
    current_time: _time.Time,
    current_session: _session.Session | None = None,
    effect: Effect,
) -> _session.Session:
    account.primary_authenticate(password=password)

    return _session.issue_session(
        account_id=account.id,
        current_time=current_time,
        current_session=current_session,
        effect=effect,
    )
