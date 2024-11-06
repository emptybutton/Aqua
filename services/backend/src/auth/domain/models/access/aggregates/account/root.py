from dataclasses import dataclass
from typing import Iterable, Literal, TypeAlias
from uuid import UUID, uuid4

from result import Err, Ok, Result

from auth.domain.framework import entity as _entity
from auth.domain.framework.effects.base import Effect
from auth.domain.models.access.aggregates.account.internal.entities import (
    account_name as _account_name,
)
from auth.domain.models.access.aggregates.account.internal.entities import (
    session as _session,
)
from auth.domain.models.access.aggregates.account.internal.specs import (
    is_account_name_taken as _is_account_name_taken,
)
from auth.domain.models.access.vos import password as _password
from auth.domain.models.access.vos import time as _time


@dataclass(kw_only=True, frozen=True, slots=True)
class PasswordChange(_entity.Mutated["Account"]):
    new_password_hash: _password.PasswordHash


AccountEvent: TypeAlias = _entity.Created["Account"] | PasswordChange


@dataclass(kw_only=True, eq=False)
class Account(_entity.Entity[UUID, AccountEvent]):
    current_name: _account_name.AccountName
    previous_names: set[_account_name.AccountName]
    sessions: set[_session.Session]
    password_hash: _password.PasswordHash

    @property
    def names(self) -> frozenset[_account_name.AccountName]:
        return frozenset({self.current_name, *self.previous_names})

    def primary_authenticate(
        self, *, password: _password.Password
    ) -> Result[None, Literal["invalid_password_for_primary_authentication"]]:
        password_hash = _password.hash_of(password)

        if self.password_hash != password_hash:
            return Err("invalid_password_for_primary_authentication")

        return Ok(None)

    def secondarily_authenticate(
        self,
        *,
        session_id: UUID,
        current_time: _time.Time,
        effect: Effect,
    ) -> Result[
        _session.Session,
        Literal[
            "no_session_for_secondary_authentication",
            "expired_session_for_secondary_authentication",
            "cancelled_session_for_secondary_authentication",
            "replaced_session_for_secondary_authentication",
        ],
    ]:
        session = self.__session_with(session_id)

        if not session:
            return Err("no_session_for_secondary_authentication")

        reasons = session.inactivity_reasons_when(current_time=current_time)

        if "replaced" in reasons:
            return Err("replaced_session_for_secondary_authentication")

        if "expired" in reasons:
            return Err("expired_session_for_secondary_authentication")

        if "cancelled" in reasons:
            return Err("cancelled_session_for_secondary_authentication")

        _session.extend(session, current_time=current_time, effect=effect)
        return Ok(session)

    @dataclass(kw_only=True, frozen=True, slots=True)
    class NameChangeOutput:
        previous_name: _account_name.AccountName | None

    async def change_name(
        self,
        *,
        new_name_text: str,
        current_time: _time.Time,
        is_account_name_taken: _is_account_name_taken.IsAccountNameTaken,
        effect: Effect,
    ) -> Result[
        NameChangeOutput,
        Literal["account_name_text_is_empty", "account_name_is_taken"],
    ]:
        if new_name_text == self.current_name.text:
            return Ok(Account.NameChangeOutput(previous_name=None))

        previous_current_name = self.current_name
        previous_name = self.__previous_name_with(text=new_name_text)
        output = Ok(
            Account.NameChangeOutput(previous_name=previous_current_name)
        )

        if previous_name:
            self.__make_previous_name_current(
                previous_name,
                current_time=current_time,
                effect=effect,
            )
            return output

        self.__make_current_name_previous(effect=effect)
        name_result = await _account_name.AccountName.create(
            text=new_name_text,
            current_time=current_time,
            account_id=self.id,
            is_account_name_taken=is_account_name_taken,
            effect=effect,
        )
        name_result.inspect(lambda name: setattr(self, "current_name", name))

        return name_result.and_then(lambda _: output)

    def change_password(
        self,
        *,
        new_password: _password.Password,
        current_session_id: UUID,
        effect: Effect,
    ) -> Result[_session.Session, Literal["no_session_for_password_change"]]:
        current_session = self.__session_with(current_session_id)

        if current_session is None:
            return Err("no_session_for_password_change")

        new_password_hash = _password.hash_of(new_password)

        if self.password_hash == new_password_hash:
            return Ok(current_session)

        self.password_hash = new_password_hash

        event = PasswordChange(entity=self, new_password_hash=new_password_hash)
        self.events.append(event)
        effect.consider(self)

        other_sessions = self.__other_sessions_when(
            current_session=current_session
        )
        for other_session in other_sessions:
            _session.cancel(other_session, effect=effect)

        return Ok(current_session)

    @dataclass(kw_only=True, frozen=True, slots=True)
    class CreationOutput:
        account: "Account"
        current_session: _session.Session

    @classmethod
    async def create(
        cls,
        *,
        name_text: str,
        password: _password.Password,
        effect: Effect,
        current_time: _time.Time,
        current_session: _session.Session | None = None,
        is_account_name_taken: _is_account_name_taken.IsAccountNameTaken,
    ) -> Result[
        CreationOutput,
        Literal["account_name_text_is_empty", "account_name_is_taken"],
    ]:
        account_id = uuid4()
        name_result = await _account_name.AccountName.create(
            text=name_text,
            current_time=current_time,
            account_id=account_id,
            is_account_name_taken=is_account_name_taken,
            effect=effect,
        )
        password_hash = _password.hash_of(password)

        current_session = _session.issue_session(
            account_id=account_id,
            current_time=current_time,
            current_session=current_session,
            effect=effect,
        )

        account_result = name_result.map(
            lambda name: Account(
                id=account_id,
                current_name=name,
                previous_names=set(),
                sessions={current_session},
                password_hash=password_hash,
                events=[],
            )
        )
        account_result.map(
            lambda account: (
                account.events.append(_entity.Created(entity=account))
            )
        )
        account_result.map(effect.consider)

        return account_result.map(
            lambda account: Account.CreationOutput(
                account=account, current_session=current_session
            )
        )

    def __session_with(self, session_id: UUID) -> _session.Session | None:
        for session in self.sessions:
            if session.id == session_id:
                return session

        return None

    def __other_sessions_when(
        self, *, current_session: _session.Session
    ) -> Iterable[_session.Session]:
        return (
            session for session in self.sessions if session != current_session
        )

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

        previous_name.become_current(current_time=current_time, effect=effect)
        self.current_name = previous_name
        self.previous_names.remove(self.current_name)


def login_to(
    account: Account,
    *,
    password: _password.Password,
    current_time: _time.Time,
    current_session: _session.Session | None = None,
    effect: Effect,
) -> Result[
    _session.Session, Literal["invalid_password_for_primary_authentication"]
]:
    result = account.primary_authenticate(password=password)

    return result.map(
        lambda _: _session.issue_session(
            account_id=account.id,
            current_time=current_time,
            current_session=current_session,
            effect=effect,
        )
    )
