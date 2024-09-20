import { adapterContainer } from "../../containers.js";
import * as _closeNotification from "../../../../application/usecases/login/close-notification.js";

export async function execute(
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    await _closeNotification.execute(
        adapterContainer.loginNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        )
    );
}
