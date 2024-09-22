import * as _views from "../../ports/views.js";
import * as _weight from "../../../domains/water-recording/value-objects/weight.js";
import * as _waterBalance from "../../../domains/water-recording/value-objects/water-balance.js";

export function execute(
    weightKilograms: number | undefined,
    targetWaterBalanceMilliliters: number | undefined,
    weightView: _views.OptionalPositiveView,
    targetWaterBalanceView: _views.OptionalPositiveView,
    notificationView: _views.RegistrationNotificationView,
): void {
    let weight: _weight.AnyWeight | undefined = undefined;
    let targetWaterBalance: _waterBalance.AnyWaterBalance | undefined = undefined;

    if (weightKilograms !== undefined)
        weight = _weight.anyWith(weightKilograms);

    if (targetWaterBalanceMilliliters !== undefined)
        targetWaterBalance = _waterBalance.anyWith(targetWaterBalanceMilliliters);

    if (targetWaterBalance !== undefined) {
        if (weight === undefined || weight instanceof _weight.Weight) {
            weightView.redrawOk();
            notificationView.redrawForValidWeightWithTargetHint();
        }
        else {
            weightView.redrawNeutral();
            notificationView.redrawForInvalidWeightWithTargetHint();
        }

        return;
    }

    if (targetWaterBalance === undefined) {
        if (weight instanceof _weight.WeightForTarget) {
            weightView.redrawOk();
            targetWaterBalanceView.redrawOk();
            notificationView.redrawForValidWeightWithoutTargetHint();
        }
        else {
            weightView.redrawNeutral();
            targetWaterBalanceView.redrawNeutral();
            notificationView.redrawForInvalidWeightWithoutTargetHint();
        }

        return;
    }
}
