import * as uuid from "../value-objects/uuid.js";
import * as water from "../value-objects/water.js";

export class Record {
    constructor(
        public id: uuid.UUID,
        public user_id: uuid.UUID,
        public drunkWater: water.Water,
        public recordingTime: Date,
    ) {}
}
