import * as _views from "../ports/views.js";
import * as _repos from "../ports/repos.js";
import * as _stages from "../ports/stages.js";
import * as _timeouts from "../ports/timeouts.js";
import * as _clients from "../ports/clients.js";
import * as _loggers from "../ports/loggers.js";
import * as _username from "../../domains/access/value-objects/username.js";
import * as _password from "../../domains/access/value-objects/password.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";

type _CurrentStage = _stages.CurrentStage<_stages.RegistrationStage>;

export function prepareNewAccountUsername(
    usernameText: string,
    passwordText: string,
    currentStage: _CurrentStage,
    usernameView: _views.ValidationView,
    notificationView: _views.RegistrationNotificationView,
    viewForNewStage: _views.PossiblyInvisibleView,
    usernamesOfRegisteredUsers: _repos.Usernames,
    timeout: _timeouts.Timeout,
    backend: _clients.Backend,
    logger: _loggers.Logger,
): void {
    let goToInvalidCredentialsStage = () => _goToInvalidCredentialsStage(
        viewForNewStage, usernameView, currentStage, timeout
    );

    if (!_isForCredentials(currentStage))
        return;

    let username = _username.anyWith(usernameText);

    if (username instanceof _username.InvalidUsername) {
        notificationView.redrawForUsernameHint(username);
        goToInvalidCredentialsStage();

        return;
    }

    if (usernamesOfRegisteredUsers.contains(username)) {
        notificationView.redrawUsernameTaken(username);
        goToInvalidCredentialsStage();

        return;
    }

    notificationView.redrawInvisible();
    usernameView.redrawOk();

    let password = _password.Password.with(passwordText);
    let isPasswordStrong = password instanceof _password.StrongPower;

    if (isPasswordStrong && currentStage.is(_stages.RegistrationStage.invalidCredentials))
        viewForNewStage.redrawVisible();
    else if (!isPasswordStrong && currentStage.is(_stages.RegistrationStage.validCredentials))
        viewForNewStage.redrawInvisible();

    timeout.doAfter(2500, async () => {
        let result = await backend.existsNamed(username);

        if (result === "error") {
            if (currentStage.is(_stages.RegistrationStage.validCredentials))
                viewForNewStage.redrawInvisible();

            currentStage.replaceWith(_stages.RegistrationStage.completed);
            usernameView.redrawNeutral();
            notificationView.redrawTryAgainLater();
            logger.logBackendIsNotWorking();

            return;
        }

        if (result.exists) {
            viewForNewStage.redrawInvisible();
            usernameView.redrawNeutral();
            notificationView.redrawUsernameTaken(username);
            usernamesOfRegisteredUsers.add(username);
            currentStage.replaceWith(_stages.RegistrationStage.invalidCredentials);
        }
    });
}

function _isForCredentials(currentStage: _CurrentStage): boolean {
    let isValidCaseStage = currentStage.is(_stages.RegistrationStage.validCredentials);
    let isInvalidCaseStage = currentStage.is(_stages.RegistrationStage.invalidCredentials);

    return isValidCaseStage || isInvalidCaseStage;
}

function _goToInvalidCredentialsStage(
    viewForNewStage: _views.PossiblyInvisibleView,
    usernameView: _views.ValidationView,
    currentStage: _CurrentStage,
    timeout: _timeouts.Timeout,
): void {
    usernameView.redrawNeutral();

    if (currentStage.is(_stages.RegistrationStage.validCredentials)) {
        timeout.doNothing();
        viewForNewStage.redrawInvisible();
        currentStage.replaceWith(_stages.RegistrationStage.invalidCredentials);
    }
}
