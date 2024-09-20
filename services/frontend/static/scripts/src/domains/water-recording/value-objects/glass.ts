import * as _water from "./water.js";

export class Glass {
    constructor(readonly capacity: _water.Water) {}
}

export class InvalidGlass {
    constructor(readonly capacity: _water.InvalidWater) {}
}

export type AnyGlass = Glass | InvalidGlass;

export function anyWith(capacityMilliliters: number): AnyGlass {
    let water = _water.anyWith(capacityMilliliters)

    let waterType = _water.isInvalid(water) ? InvalidGlass : Glass;
    return new waterType(water);
}

export function isInvalid(glass: AnyGlass): glass is InvalidGlass {
    return glass instanceof InvalidGlass;
}
