import * as _water from "./water.js";

export enum Status {
    good = 1,
    not_enough_water = 2,
    excess_water = 3,
}

export class WaterBalance {
    constructor(readonly water: _water.Water) {}
}

export class InvalidWaterBalance {
    constructor(readonly water: _water.InvalidWater) {}
}

export type AnyWaterBalance = WaterBalance | InvalidWaterBalance;

export function anyWith(milliliters: number): AnyWaterBalance {
    let water = _water.anyWith(milliliters)

    let waterType = _water.isInvalid(water) ? InvalidWaterBalance : WaterBalance;
    return new waterType(water);
}

export function isInvalid(waterBalance: AnyWaterBalance): waterBalance is InvalidWaterBalance {
    return waterBalance instanceof InvalidWaterBalance;
}
