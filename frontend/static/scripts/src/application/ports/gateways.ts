import {
    Username,
    Password,
    JWT,
    StrongPassword,
    WaterBalance,
    Glass,
    Weight,
} from "../../domain/value_objects.js";

export interface BackendGateway {
    authorize(username: Username, password: Password): Promise<
        {jwt: JWT}
        | "backendIsNotWorking"
        | "incorrectPassword"
        | "noUser"
    >,

    register(
        username: Username,
        password: StrongPassword,
        waterBalance: WaterBalance | undefined,
        glass: Glass | undefined,
        weight: Weight | undefined,
    ): Promise<
        {jwt: JWT, waterBalance: WaterBalance, glass: Glass}
        | "backendIsNotWorking"
        | "userIsAlreadyRegistered"
        | "noWeightForWaterBalance"
        | "extremeWeightForWaterBalance"
    >,
}
