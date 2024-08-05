import * as aRepos from "../../infrastructure/adapters/repos.js";
import * as aGateways from "../../infrastructure/adapters/gateways.js";
import * as aLoggers from "../../infrastructure/adapters/loggers.js";
import * as aStorages from "../../infrastructure/adapters/storages.js";
import * as aViews from "../../infrastructure/adapters/views.js";
import * as pRepos from "../../application/ports/repos.js";
import * as pGateways from "../../application/ports/gateways.js";
import * as pLoggers from "../../application/ports/loggers.js";
import * as pStorages from "../../application/ports/storages.js";
import * as pViews from "../../application/ports/views.js";

export const adapterContainer = {
    _formFieldClassNameWhenValid: "valid-form-field",
    _usernamesOfUnregisteredUsers: new aRepos.InMemoryUsernames(),

    getUsernamesOfUnregisteredUsers(): pRepos.Usernames {
        return this._usernamesOfUnregisteredUsers;
    },

    getBackendGateway(): pGateways.BackendGateway {
        return aGateways.backendHTTPGateway;
    },

    getLogger(): pLoggers.Logger {
        return aLoggers.consoleLogger;
    },

    getJWTStorage(): pStorages.JWTStorage {
        return aStorages.localJwtStorage;
    },

    getWindowView(): pViews.WindowView {
        return aViews.pageView;
    },

    getFormFieldView<ElementT extends HTMLElement>(
        element: ElementT,
    ): pViews.TernaryView {
        return new aViews.TernaryCSSView(
            element,
            this._formFieldClassNameWhenValid,
            element.className,
            element.className,
        );
    },
}
