import * as _id from "../../shared/value-objects/id.js";
import * as _water from "../value-objects/water.js";

export class Record {
    constructor(
        public id: _id.ID,
        public user_id: _id.ID,
        public drunkWater: _water.Water,
        public recordingTime: Date,
    ) {}
}
