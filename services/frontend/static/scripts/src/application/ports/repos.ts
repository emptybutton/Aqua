import * as _username from "../../domains/access/value-objects/username.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";

export interface Usernames {
    add(username: _username.Username): void,
    contains(username: _username.Username): boolean,
    remove(username: _username.Username): void,
}

export interface CredentialSet {
    add(credentials: _credentials.Credentials): void,
    contains(credentials: _credentials.Credentials): boolean,
}
