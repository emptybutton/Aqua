import * as user from "../../domain/entities/user.js";
import * as glass from "../../domain/value-objects/glass.js";
import * as uuid from "../../domain/value-objects/uuid.js";
import * as waterBalance from "../../domain/value-objects/water-balance.js";
import * as weight from "../../domain/value-objects/weight.js";
import * as _credentials from "../../domain/value-objects/credentials.js";

export interface Backend {
    login(credentials: _credentials.StrongCredentials): Promise<
        {userId: uuid.UUID}
        | "error"
        | "incorrectPassword"
        | "noUser"
    >,

    register(
        credentials: _credentials.StrongCredentials,
        targetWaterBalance: waterBalance.WaterBalance | undefined,
        glass: glass.Glass | undefined,
        weight: weight.Weight | undefined,
    ): Promise<
        user.User
        | "error"
        | "userIsAlreadyRegistered"
        | "noWeightForWaterBalance"
        | "extremeWeightForWaterBalance"
    >,
}
