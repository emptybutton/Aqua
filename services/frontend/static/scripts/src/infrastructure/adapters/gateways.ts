import * as gateways from "../../application/ports/gateways.js";
import * as vos from "../../domain/value_objects.js";

const _urls = {
    registrationURL: "/api/0.1v/user/register",
    authrizationURL: "/api/0.1v/user/authorize",
}

export const _headers = {'Content-Type': 'application/json'}

export const backendHTTPGateway: gateways.BackendGateway = {
    async authorize(username: vos.Username, password: vos.Password) {
        const response = await fetch(_urls.authrizationURL, {
            method: 'POST',
            headers: _headers,
            body: JSON.stringify({
                "username": username.text,
                "password": password.text,
            })
        })

        if (response.status === 404)
            return "noUser";
        if (response.status === 401)
            return "incorrectPassword";

        const data = await response.json();

        if (typeof data.jwt !== "string")
            return "backendIsNotWorking";

        return {jwt: new vos.JWT(data.jwt)};
    },

    async register(
        username: vos.Username,
        password: vos.StrongPassword,
        waterBalance: vos.WaterBalance | undefined,
        glass: vos.Glass | undefined,
        weight: vos.Weight | undefined,
    ) {
        const response = await fetch(_urls.registrationURL, {
            method: 'POST',
            headers: _headers,
            body: JSON.stringify({
                "username": username.text,
                "password": password.text,
                "water_balance_milliliters": waterBalance?.water.milliliters,
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
                return "backendIsNotWorking";
        }

        const jwtText = data["jwt"];
        const waterBalanceMilliliters = data["water_balance_milliliters"];
        const glassMilliliters = data["glass_milliliters"];

        if (
            typeof jwtText !== "string"
            || typeof waterBalanceMilliliters !== "number"
            || typeof glassMilliliters !== "number"
        )
            return "backendIsNotWorking";

        return {
            jwt: new vos.JWT(jwtText),
            waterBalance: new vos.WaterBalance(new vos.Water(waterBalanceMilliliters)),
            glass: new vos.Glass(new vos.Water(glassMilliliters)),
        }
    }
}
