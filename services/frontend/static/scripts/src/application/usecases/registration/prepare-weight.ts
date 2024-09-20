import * as _views from "../../ports/views.js";
import * as _weight from "../../../domains/water-recording/value-objects/weight.js";
import * as _waterBalance from "../../../domains/water-recording/value-objects/water-balance.js";

export function execute(
    weightKilograms: number | undefined,
    targetWaterBalanceMilliliters: number | undefined,
    weightView: _views.ValidationView,
    notificationView: _views.RegistrationNotificationView,
): void {
    let weight: _weight.AnyWeight | undefined = undefined;
    let targetWaterBalance: _waterBalance.AnyWaterBalance | undefined = undefined;

    if (weightKilograms !== undefined)
        weight = _weight.anyWith(weightKilograms);

    if (targetWaterBalanceMilliliters !== undefined)
        targetWaterBalance = _waterBalance.anyWith(targetWaterBalanceMilliliters);

    if (targetWaterBalance !== undefined) {
        if (_isWeightWithTargetWaterBalanceValid(weight)) {
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
        if (_isWeightWithoutTargetWaterBalanceValid(weight)) {
            weightView.redrawOk();
            notificationView.redrawForValidWeightWithoutTargetHint();
        }
        else {
            weightView.redrawNeutral();
            notificationView.redrawForInvalidWeightWithoutTargetHint();
        }

        return;
    }
}

function _isWeightWithTargetWaterBalanceValid(weight?: _weight.AnyWeight): weight is _weight.Weight {
    return weight === undefined || weight instanceof _weight.Weight;
}

function _isWeightWithoutTargetWaterBalanceValid(weight?: _weight.AnyWeight): weight is _weight.WeightForTarget {
    return weight !== undefined && weight instanceof _weight.WeightForTarget
}    
