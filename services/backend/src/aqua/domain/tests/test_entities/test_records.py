from datetime import datetime, timedelta, UTC
from uuid import uuid4

from pytest import raises

from aqua.domain import entities, value_objects as vos


def test_creation_with_not_utc_time() -> None:
    water = vos.Water(milliliters=2000)

    with raises(entities.Record.NotUTCRecordingTimeError):
        entities.Record(
            user_id=uuid4(),
            drunk_water=water,
            _recording_time=datetime.now(),
        )


def test_setting_non_utc_recording_time() -> None:
    water = vos.Water(milliliters=2000)
    record = entities.Record(user_id=uuid4(), drunk_water=water)

    with raises(entities.Record.NotUTCRecordingTimeError):
        record.recording_time = datetime.now()


def test_record_equality() -> None:
    record_id = uuid4()
    user_id = uuid4()
    drunk_water = vos.Water(milliliters=2000)
    recording_time = datetime.now(UTC) - timedelta(days=60)

    record1 = entities.Record(
        id=record_id,
        user_id=user_id,
        drunk_water=drunk_water,
        _recording_time=recording_time,
    )

    record2 = entities.Record(
        id=record_id,
        user_id=user_id,
        drunk_water=drunk_water,
        _recording_time=recording_time,
    )

    assert record1 == record2
