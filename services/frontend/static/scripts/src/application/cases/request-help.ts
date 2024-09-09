import * as views from "../ports/views.js";

export async function requestHelp(
    notificationView: views.LoginNotificationView,
): Promise<void> {
    notificationView.redrawHelp();
}
