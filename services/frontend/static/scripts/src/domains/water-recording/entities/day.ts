import * as _id from "../../shared/value-objects/id.js";
import * as _waterBalance from "../value-objects/water-balance.js";

export class Day {
    constructor(
        public date: Date,
        public user_id: _id.ID,
        public targetWaterBalance: _waterBalance.WaterBalance,
        public realWaterBalance: _waterBalance.WaterBalance,
        public result: _waterBalance.Status,
    ) {}
}
