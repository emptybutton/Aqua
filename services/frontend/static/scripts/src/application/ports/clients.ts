import * as _id from "../../domains/shared/value-objects/id.js";
import * as _user from "../../domains/water-recording/entities/user.js";
import * as _glass from "../../domains/water-recording/value-objects/glass.js";
import * as _waterBalance from "../../domains/water-recording/value-objects/water-balance.js";
import * as _weight from "../../domains/water-recording/value-objects/weight.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";
import * as _username from "../../domains/access/value-objects/username.js";
import * as _account from "../../domains/access/entities/account.js";

export type Result<T> = Promise<T | "error">

export interface Backend {
    login(credentials: _credentials.StrongCredentials): Result<
        {userId: _id.ID}
        | "incorrectPassword"
        | "noUser"
    >,

    register(
        credentials: _credentials.StrongCredentials,
        targetWaterBalance: _waterBalance.WaterBalance,
        weight: _weight.Weight | undefined,
        glass: _glass.Glass | undefined,
    ): Result<
        {user: _user.User, account: _account.Account} | "userIsAlreadyRegistered"
    >,
    register(
        credentials: _credentials.StrongCredentials,
        targetWaterBalance: undefined,
        weight: _weight.WeightForTarget,
        glass: _glass.Glass | undefined,
    ): Result<
        {user: _user.User, account: _account.Account} | "userIsAlreadyRegistered"
    >,

    existsNamed(username: _username.Username): Result<{exists: boolean}>,
}
