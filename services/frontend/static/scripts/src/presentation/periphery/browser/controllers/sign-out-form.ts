import * as logout from "../../../di/facade/logout.js";

export function constructControllers(
    buttonElement: HTMLElement,
): void {
    const handle = async () => await logout.perform();
    buttonElement.addEventListener("onclick", handle);
}
