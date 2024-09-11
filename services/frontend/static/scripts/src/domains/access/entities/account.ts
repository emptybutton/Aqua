import * as _username from "../value-objects/username.js";
import * as _id from "../../shared/value-objects/id.js";

export class Account {
    constructor(
        public id: _id.ID,
        public username: _username.Username,
    ) {}
}
