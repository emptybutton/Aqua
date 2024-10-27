from datetime import UTC, datetime
from uuid import UUID

from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.framework.entity import Created, FrozenEntities
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water


def test_result() -> None:
    user_id = UUID(int=4)
    drunk_water = Water.with_(milliliters=10).unwrap()
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()

    result = Record.create(
        user_id=user_id,
        drunk_water=drunk_water,
        current_time=current_time,
        effect=SearchableEffect(),
    )

    assert result.user_id == user_id
    assert result.drunk_water == drunk_water
    assert result.recording_time == current_time
    assert not result.is_cancelled
    assert result.events == [Created(entity=result)]


def test_effect() -> None:
    user_id = UUID(int=4)
    drunk_water = Water.with_(milliliters=10).unwrap()
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()
    effect = SearchableEffect()

    result = Record.create(
        user_id=user_id,
        drunk_water=drunk_water,
        current_time=current_time,
        effect=effect,
    )

    assert effect.entities_that(Record) == FrozenEntities([result])
