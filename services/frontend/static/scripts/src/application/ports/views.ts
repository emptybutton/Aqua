import * as _username from "../../domains/access/value-objects/username.js";
import * as _password from "../../domains/access/value-objects/password.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";

export interface WindowView {
    redrawToLogin(): void,
    redrawForMainInteractions(): void,
}

export interface LoginNotificationView {
    redrawInvisible(): void,
    redrawNoUserWithUsername(username: _username.AnyUsername): void,
    redrawInvalidCredentials(credentials: _credentials.Credentials): void,
    redrawLastTimeThereWasNoUserNamed(username: _username.AnyUsername): void,
    redrawLastTimeThereWasNoUserWithCredentials(
        credentials: _credentials.Credentials,
    ): void,
    redrawInvalidUsername(username: _username.AnyUsername): void,
    redrawInvalidPassword(password: _password.Password): void,
    redrawTryAgainLater(): void,
}

export interface ValidationView {
    redrawOk(): void,
    redrawNeutral(): void,
}
