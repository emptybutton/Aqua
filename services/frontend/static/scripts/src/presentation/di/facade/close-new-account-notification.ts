import { adapterContainer } from "../containers.js";
import * as _closeNewAccountNotification from "../../../application/cases/close-new-account-notification.js";

export async function closeNewAccountNotification(
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    await _closeNewAccountNotification.closeNewAccountNotification(
        adapterContainer.registrationNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        )
    );
}
