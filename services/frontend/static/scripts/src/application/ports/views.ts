import * as _username from "../../domains/access/value-objects/username.js";
import * as _password from "../../domains/access/value-objects/password.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";
import * as _weight from "../../domains/water-recording/value-objects/weight.js";
import * as _waterBalance from "../../domains/water-recording/value-objects/water-balance.js";
import * as _glass from "../../domains/water-recording/value-objects/glass.js";

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

export interface RegistrationNotificationView {
    redrawInvisible(): void,
    redrawForUsernameHint(username: _username.AnyUsername): void,
    redrawForTakenUsernameHint(username: _username.AnyUsername): void,
    redrawUsernameTaken(username: _username.AnyUsername): void,
    redrawForPasswordHint(password: _password.Password): void,
    redrawForWeightWithTargetHint(weight: _weight.AnyWeight): void,
    redrawForWeightWithoutTargetHint(weight: _weight.AnyWeight): void,
    redrawForTargetWithWeightHint(waterBalance: _waterBalance.AnyWaterBalance): void,
    redrawForTargetWithoutWeightHint(waterBalance: _waterBalance.AnyWaterBalance): void,
    redrawForGlassHint(glass: _glass.AnyGlass): void,
    redrawTryAgainLater(): void,
}

export interface ValidationView {
    redrawOk(): void,
    redrawNeutral(): void,
}
