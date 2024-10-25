from aqua.domain.model.core.vos.target import Result


class UnhandledResultError: ...


def new_result_view_of(result: Result) -> str:
    match result:
        case Result.good:
            return "good"
        case Result.not_enough_water:
            return "not_enough_water"
        case Result.excess_water:
            return "excess_water"
        case _:
            raise UnhandledResultError


def old_result_view_of(result: Result) -> int:
    match result:
        case Result.good:
            return 1
        case Result.not_enough_water:
            return 2
        case Result.excess_water:
            return 3
        case _:
            raise UnhandledResultError
