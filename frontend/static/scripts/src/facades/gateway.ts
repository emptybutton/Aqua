import {
    Username,
    Password,
    StrongPassword,
    WaterBalance,
    Glass,
    Weight,
    Water,
} from "../domain/value_objects";

const _urls = {
    registrationURL: "/api/0.1v/user/register",
    authrizationURL: "/api/0.1v/user/authorize",
}

export const _headers = {'Content-Type': 'application/json'}

export async function authorize(
    username: Username,
    password: Password,
) {
    const response = await fetch(_urls.authrizationURL, {
      method: 'POST',
      headers: _headers,
      body: JSON.stringify({
              "username": username.text,
              "password": password.text,
        })
    })

    if (!response.ok)
        return;

    const data = await response.json();
    const jwt = data["jwt"];

    if (typeof jwt === "string")
        return {jwt: jwt};
}

export async function register(
    username: Username,
    password: StrongPassword,
    waterBalance: WaterBalance | undefined,
    glass: Glass | undefined,
    weight: Weight | undefined,
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

    if (!response.ok)
        return;

    const data = await response.json();

    const jwt = data["jwt"];
    const waterBalanceMilliliters = data["water_balance_milliliters"];
    const glassMilliliters = data["glass_milliliters"];

    if (
        typeof jwt !== "string"
        || typeof waterBalanceMilliliters !== "number"
        || typeof glassMilliliters !== "number"
    )
        return;

    return {
        jwt: jwt,
        waterBalance: new WaterBalance(new Water(waterBalanceMilliliters)),
        glass: new Glass(new Water(glassMilliliters)),
    }
}
