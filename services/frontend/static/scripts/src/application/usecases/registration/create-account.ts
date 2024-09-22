import * as _views from "../../ports/views.js";
import * as _repos from "../../ports/repos.js";
import * as _clients from "../../ports/clients.js";
import * as _timeouts from "../../ports/timeouts.js";
import * as _loggers from "../../ports/loggers.js";
import * as _username from "../../../domains/access/value-objects/username.js";
import * as _password from "../../../domains/access/value-objects/password.js";
import * as _credentials from "../../../domains/access/value-objects/credentials.js";
import * as _weight from "../../../domains/water-recording/value-objects/weight.js";
import * as _waterBalance from "../../../domains/water-recording/value-objects/water-balance.js";
import * as _glass from "../../../domains/water-recording/value-objects/glass.js";

export async function execute(
    usernameText: string,
    passwordText: string,
    weightKilograms: number | undefined,
    targetWaterBalanceMilliliters: number | undefined,
    glassCapacityMilliliters: number | undefined,
    notificationView: _views.RegistrationNotificationView,
    usernameView: _views.OptionalPositiveView,
    windowView: _views.WindowView,
    executingView: _views.TernaryView,
    executingViewTimeout: _timeouts.Timeout,
    windowViewTimeout: _timeouts.Timeout,
    usernamesOfRegisteredUsers: _repos.Usernames,
    backend: _clients.Backend,
    logger: _loggers.Logger,
): Promise<void> {
    let showExecutingViewBad = () => _showExecutingViewBad(executingView, executingViewTimeout);

    let username = _username.anyWith(usernameText);
    let password = _password.Password.with(passwordText);
    let credentials = new _credentials.Credentials(username, password);

    if (
        !_credentials.isStrong(credentials)
        || usernamesOfRegisteredUsers.contains(username)
    ) {
        showExecutingViewBad();
        return;
    }

    let weight: _weight.AnyWeight | undefined = undefined;
    let targetWaterBalance: _waterBalance.AnyWaterBalance | undefined = undefined;
    let glass: _glass.AnyGlass | undefined = undefined;

    if (weightKilograms !== undefined)
        weight = _weight.anyWith(weightKilograms);

    if (targetWaterBalanceMilliliters !== undefined)
        targetWaterBalance = _waterBalance.anyWith(targetWaterBalanceMilliliters);

    if (glassCapacityMilliliters !== undefined)
        glass = _glass.anyWith(glassCapacityMilliliters)

    let asyncResult: ReturnType<_clients.Backend["register"]>;

    if (
        targetWaterBalance === undefined
        && weight instanceof _weight.WeightForTarget
    )
        asyncResult = backend.register(credentials, targetWaterBalance, weight, glass);
    else if (targetWaterBalance === undefined) {
        showExecutingViewBad();
        return;
    }
    else
        asyncResult = backend.register(credentials, targetWaterBalance, weight, glass);

    let result = await asyncResult;

    if (result === "error") {
        showExecutingViewBad();
        logger.logBackendIsNotWorking();
        notificationView.redrawTryAgainLater();
    }
    else if (result === "userIsAlreadyRegistered") {
        usernamesOfRegisteredUsers.add(username);
        usernameView.redrawNeutral();
        executingView.redrawBad();
        notificationView.redrawUsernameTaken(username);
    }
    else {
        notificationView.redrawAccountCreated();
        executingView.redrawOk();
        executingViewTimeout.doNothing();
        windowViewTimeout.doAfter(3000, () => {
            windowView.redrawForMainInteractions();
        });
    }
}

function _showExecutingViewBad(
    executingView: _views.TernaryView,
    executingViewTimeout: _timeouts.Timeout,
): void {
    executingView.redrawBad();
    executingViewTimeout.doAfter(3000, () => executingView.redrawNeutral());
}
