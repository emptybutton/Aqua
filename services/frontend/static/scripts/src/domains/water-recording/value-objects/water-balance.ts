import { Water } from "./water.js";

export enum Status {
    good = 1,
    not_enough_water = 2,
    excess_water = 3,
}

export class WaterBalance {
    constructor(readonly water: Water) {}
}
