import * as glass from "../value-objects/glass.js";
import * as username from "../value-objects/username.js";
import * as uuid from "../value-objects/uuid.js";
import * as waterBalance from "../value-objects/water-balance.js";
import * as weight from "../value-objects/weight.js";

export class User {
    constructor(
        public id: uuid.UUID,
        public name: username.Username,
        public targetWaterBalance: waterBalance.WaterBalance,
        public glass: glass.Glass,
        public weight: weight.Weight | undefined,
    ) {}
}
