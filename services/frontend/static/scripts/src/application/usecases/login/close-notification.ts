import * as views from "../../ports/views.js";

export async function execute(
    notificationView: views.LoginNotificationView,
): Promise<void> {
    notificationView.redrawInvisible();
}
