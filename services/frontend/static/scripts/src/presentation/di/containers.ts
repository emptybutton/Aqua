import * as aRepos from "../../infrastructure/adapters/repos.js";
import * as aClients from "../../infrastructure/adapters/clients.js";
import * as aLoggers from "../../infrastructure/adapters/loggers.js";
import * as aViews from "../../infrastructure/adapters/views.js";
import * as aTimeouts from "../../infrastructure/adapters/timeouts.js";
import * as pRepos from "../../application/ports/repos.js";
import * as pClients from "../../application/ports/clients.js";
import * as pLoggers from "../../application/ports/loggers.js";
import * as pViews from "../../application/ports/views.js";
import * as pTimeouts from "../../application/ports/timeouts.js";

export const adapterContainer = {
    _formFieldClassNameWhenNeutral: "",
    _formFieldClassNameWhenOK: "valid-form-field",
    _buttonClassNameWhenOK: "ok-button",
    _buttonClassNameWhenNeutral: "",
    _buttonClassNameWhenBad: "bad-button",
    _usernamesOfUnregisteredUsers: new aRepos.InMemoryUsernames(),
    _usernamesOfRegisteredUsers: new aRepos.InMemoryUsernames(),
    _invalidCredentialSet: new aRepos.InMemoryCredentialSet(),
    _timeoutForUsernameAvailability: new aTimeouts.InMemoryTimeout(),
    _redirectionTimeout: new aTimeouts.InMemoryTimeout(),
    _registrationButtonTimeout: new aTimeouts.InMemoryTimeout(),

    get usernamesOfRegisteredUsers(): pRepos.Usernames {
        return this._usernamesOfRegisteredUsers;
    },

    get usernamesOfUnregisteredUsers(): pRepos.Usernames {
        return this._usernamesOfUnregisteredUsers;
    },

    get invalidCredentialSet(): pRepos.CredentialSet {
        return this._invalidCredentialSet;
    },

    get backend(): pClients.Backend {
        return aClients.backendAPI;
    },

    get logger(): pLoggers.Logger {
        return aLoggers.consoleLogger;
    },

    get windowView(): pViews.WindowView {
        return aViews.pageView;
    },

    get timeoutForUsernameAvailability(): pTimeouts.Timeout {
        return this._timeoutForUsernameAvailability;
    },

    get redirectionTimeout(): pTimeouts.Timeout {
        return this._redirectionTimeout;
    },
    
    get registrationButtonTimeout(): pTimeouts.Timeout {
        return this._registrationButtonTimeout;
    },

    formFieldViewOf(element: HTMLElement): pViews.OptionalPositiveView {
        return new aViews.OptionalPositiveCSSView(
            element,
            this._formFieldClassNameWhenOK,
            this._formFieldClassNameWhenNeutral,
        );
    },

    buttonTernaryViewOf(element: HTMLElement): pViews.TernaryView {
        return new aViews.TernaryCSSView(
            element,
            this._buttonClassNameWhenOK,
            this._buttonClassNameWhenNeutral,
            this._buttonClassNameWhenBad,
        );
    },

    loginNotificationViewOf(
        signalElement: HTMLElement,
        textElement: HTMLElement,
    ): pViews.LoginNotificationView {
        return new aViews.LoginDefaultNotificationCSSView(signalElement, textElement);
    },

    registrationNotificationViewOf(
        signalElement: HTMLElement,
        textElement: HTMLElement,
    ): pViews.RegistrationNotificationView {
        return new aViews.RegistrationDefaultNotificationCSSView(signalElement, textElement)
    }
}
