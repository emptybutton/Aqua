import * as _password from "./password.js";
import * as _username from "./username.js";

export class Credentials<
    UsernameT extends _username.AnyUsername = _username.AnyUsername,
    PasswordT extends _password.Password = _password.Password
> {
    constructor(
        readonly username: UsernameT,
        readonly password: PasswordT,
    ) {}
}

export type StrongCredentials = Credentials<
    _username.Username,
    _password.StrongPassword
>;
