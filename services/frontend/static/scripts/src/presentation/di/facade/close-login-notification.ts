import { adapterContainer } from "../containers.js";
import * as _closeLoginNotification from "../../../application/cases/close-login-notification.js";


export async function closeLoginNotification(
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    await _closeLoginNotification.closeLoginNotification(
        adapterContainer.loginNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        )
    );
}
