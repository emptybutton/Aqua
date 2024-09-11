import * as _id from "../../shared/value-objects/id.js";
import * as _glass from "../value-objects/glass.js";
import * as _waterBalance from "../value-objects/water-balance.js";
import * as _weight from "../value-objects/weight.js";

export class User {
    constructor(
        public id: _id.ID,
        public targetWaterBalance: _waterBalance.WaterBalance,
        public glass: _glass.Glass,
        public weight: _weight.Weight | undefined,
    ) {}
}
