from datetime import UTC, date, datetime, timedelta

from aqua.infrastructure.periphery.pymongo.document import Document


def in_date_range(date_: date) -> Document:
    datetime_ = datetime(date_.year, date_.month, date_.day, tzinfo=UTC)

    return {
        "$gte": datetime_,
        "$lt": datetime_ + timedelta(days=1),
    }
