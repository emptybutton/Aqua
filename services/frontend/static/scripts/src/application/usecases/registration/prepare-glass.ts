import * as _views from "../../ports/views.js";
import * as _glass from "../../../domains/water-recording/value-objects/glass.js";

export function execute(
    glassCapacityMilliliters: number | undefined,
    glassView: _views.ValidationView,
    notificationView: _views.RegistrationNotificationView,
): void {
    let glass: _glass.AnyGlass | undefined = undefined;

    if (glassCapacityMilliliters !== undefined)
        glass = _glass.anyWith(glassCapacityMilliliters);

    if (glass instanceof _glass.InvalidGlass) {
        glassView.redrawNeutral();
        notificationView.redrawForInvalidGlassHint();
    }
    else {
        glassView.redrawOk();
        notificationView.redrawForValidGlassHint();

    }
}
