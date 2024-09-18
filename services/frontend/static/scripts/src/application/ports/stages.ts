export enum RegistrationStage {
    validCredentials,
    invalidCredentials,
    validWeight,
    invalidWeight,
    validTargetWaterBalance,
    invalidTargetWaterBalance,
    validGlass,
    invalidGlass,
    completed,
}

export interface CurrentStage<StageT> {
    is(stage: StageT): boolean,
    replaceWith(newStage: StageT): void,
}
