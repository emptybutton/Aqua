import { adapterContainer } from "../containers.js";
import * as _closeLoginNotification from "../../../application/cases/close-login-notification.js";


export async function closeLoginNotification(
    notificationElement: HTMLElement,
): Promise<void> {
    await _closeLoginNotification.closeLoginNotification(
        adapterContainer.loginNotificationViewOf(notificationElement)
    );
}
