import * as views from "../ports/views.js";

export async function closeLoginNotification(
    notificationView: views.LoginNotificationView,
): Promise<void> {
    notificationView.redrawInvisible();
}
