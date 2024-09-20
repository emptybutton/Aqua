import { adapterContainer } from "../../containers.js";
import * as _prepareGlass from "../../../../application/usecases/registration/prepare-glass.js";

export async function execute(
    glassCapacityMilliliters: number | undefined,
    glassFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    _prepareGlass.execute(
        glassCapacityMilliliters,
        adapterContainer.formFieldViewOf(glassFieldElement),
        adapterContainer.registrationNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
    )
}
