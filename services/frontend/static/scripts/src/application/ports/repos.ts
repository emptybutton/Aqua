import * as _username from "../../domain/value-objects/username.js";
import * as _credentials from "../../domain/value-objects/credentials.js";

export interface Usernames {
    add(username: _username.Username): void,
    contains(username: _username.Username): boolean,
}

export interface CredentialSet {
    add(credentials: _credentials.Credentials): void,
    contains(credentials: _credentials.Credentials): boolean,
}
