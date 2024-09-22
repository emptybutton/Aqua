import * as _views from "../../ports/views.js";
import * as _weight from "../../../domains/water-recording/value-objects/weight.js";
import * as _waterBalance from "../../../domains/water-recording/value-objects/water-balance.js";

export function execute(
    targetWaterBalanceMilliliters: number | undefined,
    weightKilograms: number | undefined,
    targetWaterBalanceView: _views.OptionalPositiveView,
    weightView: _views.OptionalPositiveView,
    notificationView: _views.RegistrationNotificationView,
): void {
    let weight: _weight.AnyWeight | undefined = undefined;
    let targetWaterBalance: _waterBalance.AnyWaterBalance | undefined = undefined;

    if (weightKilograms !== undefined)
        weight = _weight.anyWith(weightKilograms);

    if (targetWaterBalanceMilliliters !== undefined)
        targetWaterBalance = _waterBalance.anyWith(targetWaterBalanceMilliliters);

    if (targetWaterBalance instanceof _waterBalance.WaterBalance) {
        targetWaterBalanceView.redrawOk();

        if (weight instanceof _weight.WeightForTarget) {
            weightView.redrawOk();
            notificationView.redrawForValidTargetWithWeightHint();
        }
        else if (weight === undefined || weight instanceof _weight.Weight) {
            weightView.redrawOk();
            notificationView.redrawForValidTargetWithoutWeightHint();
        }
        else if (weight instanceof _weight.InvalidWeight) {
            weightView.redrawNeutral();
            notificationView.redrawForValidTargetWithoutWeightHint();
        }
    }
    else {
        if (weight instanceof _weight.WeightForTarget) {
            targetWaterBalanceView.redrawOk();
            notificationView.redrawForValidTargetWithWeightHint();
        }
        else {
            targetWaterBalanceView.redrawNeutral();
            weightView.redrawNeutral();
            notificationView.redrawForInvalidTargetWithoutWeightHint();
        }
    }
}
