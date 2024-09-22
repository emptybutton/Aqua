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

export function isStrong(credentials: Credentials): credentials is StrongCredentials {
    let isUsernameOk = credentials.username instanceof _username.Username;
    let isPasswordOk = credentials.password.power instanceof _password.StrongPower;

    return isUsernameOk && isPasswordOk;
}
