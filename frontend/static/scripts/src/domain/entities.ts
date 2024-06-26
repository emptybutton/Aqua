import {
    Username,
    WaterBalance,
    Glass,
    Weight,
    Water,
    UUID,
    WaterBalanceStatus,
} from "./value_objects.js";

export class User {
    constructor(
        public id: UUID,
        public name: Username,
        public targetWaterBalance: WaterBalance,
        public glass: Glass,
        public weight: Weight | undefined,
    ) {}
}

export class Record {
    constructor(
        public id: UUID,
        public user_id: UUID,
        public drunkWater: Water,
        public recordingTime: Date,
    ) {}
}

export class Day {
    constructor(
        public date: Date,
        public user_id: UUID,
        public targetWaterBalance: WaterBalance,
        public realWaterBalance: WaterBalance,
        public result: WaterBalanceStatus,
    ) {}
}
