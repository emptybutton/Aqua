from datetime import UTC, datetime
from uuid import uuid4

from pytest import fixture
from result import Err, Ok

from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.framework.entity import FrozenEntities
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Cancelled,
    CancelledRecordToCancelError,
    Record,
    cancel,
)
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water


@fixture
def not_cancelled_record() -> Record:
    return Record(
        id=uuid4(),
        events=list(),
        user_id=uuid4(),
        drunk_water=Water.with_(milliliters=500).unwrap(),
        recording_time=Time.with_(datetime_=datetime.now(UTC)).unwrap(),
        is_cancelled=False,
    )


@fixture
def cancelled_record() -> Record:
    return Record(
        id=uuid4(),
        events=list(),
        user_id=uuid4(),
        drunk_water=Water.with_(milliliters=500).unwrap(),
        recording_time=Time.with_(datetime_=datetime.now(UTC)).unwrap(),
        is_cancelled=True,
    )


def test_result_with_not_cancelled(not_cancelled_record: Record) -> None:
    result = cancel(not_cancelled_record, effect=SearchableEffect())

    assert result == Ok(None)


def test_with_not_cancelled(not_cancelled_record: Record) -> None:
    cancel(not_cancelled_record, effect=SearchableEffect())

    assert not_cancelled_record.is_cancelled


def test_events_with_not_cancelled(not_cancelled_record: Record) -> None:
    cancel(not_cancelled_record, effect=SearchableEffect())

    events = [Cancelled(entity=not_cancelled_record)]
    assert not_cancelled_record.events == events


def test_effect_with_not_cancelled(not_cancelled_record: Record) -> None:
    effect = SearchableEffect()
    cancel(not_cancelled_record, effect=effect)

    entities = effect.entities_that(Record)
    assert entities == FrozenEntities([not_cancelled_record])


def test_result_with_cancelled(cancelled_record: Record) -> None:
    result = cancel(cancelled_record, effect=SearchableEffect())

    assert result == Err(CancelledRecordToCancelError())
