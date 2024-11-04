from datetime import date, datetime, timezone

from aqua.infrastructure.periphery.pymongo.document import (
    DocumentDate,
    DocumentDatetime,
)


def native_date_of(document_date: DocumentDate) -> date:
    return date(document_date.year, document_date.month, document_date.day)


def native_datetime_of(document_datetime: DocumentDatetime) -> datetime:
    tz = document_datetime.tzinfo
    timedelta = None if tz is None else tz.utcoffset(None)
    native_tz = None if timedelta is None else timezone(timedelta)

    return datetime(
        document_datetime.year,
        document_datetime.month,
        document_datetime.day,
        document_datetime.hour,
        document_datetime.minute,
        document_datetime.second,
        document_datetime.microsecond,
        native_tz,
        fold=document_datetime.fold,
    )
