import * as _clients from "../../application/ports/clients.js";
import * as _id from "../../domains/shared/value-objects/id.js";
import * as _user from "../../domains/water-recording/entities/user.js";
import * as _glass from "../../domains/water-recording/value-objects/glass.js";
import * as _waterBalance from "../../domains/water-recording/value-objects/water-balance.js";
import * as _water from "../../domains/water-recording/value-objects/water.js";
import * as _weight from "../../domains/water-recording/value-objects/weight.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";
import * as _account from "../../domains/access/entities/account.js";
import * as _username from "../../domains/access/value-objects/username.js";
import { maybe } from "../../domains/shared/value-objects/maybe.js";

const _urls = {
    registrationURL: "/api/0.1v/user/register",
    authrizationURL: "/api/0.1v/user/authorize",
}

export const _headers = {'Content-Type': 'application/json'}

export const backendAPI: _clients.Backend = {
    async login(credentials: _credentials.StrongCredentials): Promise<
        {userId: _id.ID}
        | "error"
        | "incorrectPassword"
        | "noUser"
    > {
        const response = await fetch(_urls.authrizationURL, {
            method: 'POST',
            headers: _headers,
            body: JSON.stringify({
                "username": credentials.username.text,
                "password": credentials.password.text,
            })
        })

        if (response.status === 404)
            return "noUser";
        if (response.status === 401)
            return "incorrectPassword";

        const data = await response.json();
        const userId = data["user_id"];

        if (typeof userId !== "string")
            return "error";

        return {userId: userId};
    },

    async register(
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
    > {
        const response = await fetch(_urls.registrationURL, {
            method: 'POST',
            headers: _headers,
            body: JSON.stringify({
                "username": credentials.username.text,
                "password": credentials.password.text,
                "water_balance_milliliters": targetWaterBalance?.water.milliliters,
                "glass_milliliters": glass?.capacity.milliliters,
                "weight_kilograms": weight?.kilograms,
            })
        })

        const data = await response.json();

        if (!response.ok) {
            const errorType = data?.detail?.[0]?.type;

            if (errorType === "UserIsAlreadyRegisteredError")
                return "userIsAlreadyRegistered";

            else if (errorType === "NoWeightForWaterBalanceError")
                return "noWeightForWaterBalance";

            else if (errorType === "ExtremeWeightForWaterBalanceError")
                return "extremeWeightForWaterBalance";

            else 
                return "error";
        }

        const userId = data["user_id"];
        const usernameText = data["username"];
        const targetWaterBalanceMilliliters = data["target_water_balance_milliliters"];
        const glassMilliliters = data["glass_milliliters"];
        const weightKilograms = data["weight_kilograms"];

        if (!(
            typeof userId === "string"
            && typeof usernameText === "string"
            && typeof targetWaterBalanceMilliliters === "number"
            && typeof glassMilliliters === "number"
            && ((typeof weightKilograms === "number") || weightKilograms === null)
        ))
            return "error";

        const user = maybe(() => new _user.User(
            userId,
            new _waterBalance.WaterBalance(new _water.Water(targetWaterBalanceMilliliters)),
            new _glass.Glass(new _water.Water(glassMilliliters)),
            weightKilograms === null ? undefined : new _weight.Weight(weightKilograms),
        ));

        const account = maybe(() => new _account.Account(
            userId,
            new _username.Username(usernameText),
        ));

        if (user === undefined || account === undefined)
            return "error"

        return {user: user, account: account};
    }
}
