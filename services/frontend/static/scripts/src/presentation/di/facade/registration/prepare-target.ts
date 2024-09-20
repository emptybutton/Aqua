import { adapterContainer } from "../../containers.js";
import * as _prepareTarget from "../../../../application/usecases/registration/prepare-target.js";

export function execute(
    targetWaterBalanceMilliliters: number | undefined,
    weightKilograms: number | undefined,
    targetWaterBalanceFieldElement: HTMLElement,
    weightFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): void {
    _prepareTarget.execute(
        targetWaterBalanceMilliliters,
        weightKilograms,
        adapterContainer.formFieldViewOf(targetWaterBalanceFieldElement),
        adapterContainer.formFieldViewOf(weightFieldElement),
        adapterContainer.registrationNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
    )
}
