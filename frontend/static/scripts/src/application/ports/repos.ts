import { Username } from "../../domain/value_objects.js";

export interface Usernames {
    add(username: Username): void,
    contains(username: Username): boolean,
}
