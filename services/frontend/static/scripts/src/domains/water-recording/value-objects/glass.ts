import * as _water from "./water.js";

export class Glass {
    constructor(readonly capacity: _water.Water) {}
}

export class InvalidGlass {
    constructor(readonly capacity: _water.InvalidWater) {}
}

export type AnyGlass = Glass | InvalidGlass;
