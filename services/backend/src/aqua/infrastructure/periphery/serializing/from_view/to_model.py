from aqua.domain.model.core.vos.target import Result


def result_of_new(result_view: str) -> Result | None:
    match result_view:
        case "good":
            return Result.good
        case "not_enough_water":
            return Result.not_enough_water
        case "excess_water":
            return Result.excess_water
        case _:
            return None


def result_of_old(result_view: int) -> Result | None:
    match result_view:
        case 1:
            return Result.good
        case 2:
            return Result.not_enough_water
        case 3:
            return Result.excess_water
        case _:
            return None
