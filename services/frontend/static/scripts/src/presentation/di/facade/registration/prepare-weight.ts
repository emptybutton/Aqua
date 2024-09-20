import { adapterContainer } from "../../containers.js";
import * as _prepareWeight from "../../../../application/usecases/registration/prepare-weight.js";

export function execute(
    weightKilograms: number | undefined,
    targetWaterBalanceMilliliters: number | undefined,
    weightFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): void {
    _prepareWeight.execute(
        weightKilograms,
        targetWaterBalanceMilliliters,
        adapterContainer.formFieldViewOf(weightFieldElement),
        adapterContainer.registrationNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
    )
}
