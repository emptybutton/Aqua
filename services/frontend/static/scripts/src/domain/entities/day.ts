import * as uuid from "../value-objects/uuid.js";
import * as waterBalance from "../value-objects/water-balance.js";

export class Day {
    constructor(
        public date: Date,
        public user_id: uuid.UUID,
        public targetWaterBalance: waterBalance.WaterBalance,
        public realWaterBalance: waterBalance.WaterBalance,
        public result: waterBalance.Status,
    ) {}
}
