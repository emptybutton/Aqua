from typing import Any


type Value = dict[str, Any]
type Values = list[Value]


def updating(values: Values) -> Values:
    return [{f"{k}_": v for k, v in value.items()} for value in values]
