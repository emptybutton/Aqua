import * as uuid from "../value-objects/uuid";
import * as water from "../value-objects/water";

export class Record {
    constructor(
        public id: uuid.UUID,
        public user_id: uuid.UUID,
        public drunkWater: water.Water,
        public recordingTime: Date,
    ) {}
}
