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
    _usernamesOfUnregisteredUsers: new aRepos.InMemoryUsernames(),
    _usernamesOfRegisteredUsers: new aRepos.InMemoryUsernames(),
    _invalidCredentialSet: new aRepos.InMemoryCredentialSet(),
    _timeoutForUsernameAvailability: new aTimeouts.InMemoryTimeout(),

    get usernamesOfRegisteredUsers(): pRepos.Usernames {
        return this._usernamesOfUnregisteredUsers;
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

    formFieldViewOf(element: HTMLElement): pViews.ValidationView {
        return new aViews.ValidationCSSView(
            element,
            this._formFieldClassNameWhenOK,
            this._formFieldClassNameWhenNeutral,
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
