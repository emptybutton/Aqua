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
