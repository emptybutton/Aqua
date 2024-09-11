import * as _id from "../../domains/shared/value-objects/id.js";
import * as _user from "../../domains/water-recording/entities/user.js";
import * as _glass from "../../domains/water-recording/value-objects/glass.js";
import * as _waterBalance from "../../domains/water-recording/value-objects/water-balance.js";
import * as _weight from "../../domains/water-recording/value-objects/weight.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";
import * as _account from "../../domains/access/entities/account.js";

export interface Backend {
    login(credentials: _credentials.StrongCredentials): Promise<
        {userId: _id.ID}
        | "error"
        | "incorrectPassword"
        | "noUser"
    >,

    register(
        credentials: _credentials.StrongCredentials,
        targetWaterBalance: _waterBalance.WaterBalance | undefined,
        glass: _glass.Glass | undefined,
        weight: _weight.Weight | undefined,
    ): Promise<
        {user: _user.User, account: _account.Account}
        | "error"
        | "userIsAlreadyRegistered"
        | "noWeightForWaterBalance"
        | "extremeWeightForWaterBalance"
    >,
}
