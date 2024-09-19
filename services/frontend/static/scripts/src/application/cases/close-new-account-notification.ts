import * as views from "../ports/views.js";

export async function closeNewAccountNotification(
    notificationView: views.RegistrationNotificationView,
): Promise<void> {
    notificationView.redrawInvisible();
}
