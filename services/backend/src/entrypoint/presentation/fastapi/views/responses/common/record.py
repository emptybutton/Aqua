from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from entrypoint.infrastructure.clients.aqua import RecordData


class RecordSchema(BaseModel):
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime

    @classmethod
    def of(cls, record_data: RecordData) -> "RecordSchema":
        return RecordSchema(
            record_id=record_data.record_id,
            drunk_water_milliliters=record_data.drunk_water_milliliters,
            recording_time=record_data.recording_time,
        )
