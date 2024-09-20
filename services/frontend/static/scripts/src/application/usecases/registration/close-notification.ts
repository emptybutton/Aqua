import * as views from "../../ports/views.js";

export async function execute(
    notificationView: views.RegistrationNotificationView,
): Promise<void> {
    notificationView.redrawInvisible();
}
