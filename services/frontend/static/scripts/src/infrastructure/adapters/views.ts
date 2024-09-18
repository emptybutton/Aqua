import * as views from "../../application/ports/views.js";
import * as _username from "../../domains/access/value-objects/username.js";
import * as _password from "../../domains/access/value-objects/password.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";
import * as _weight from "../../domains/water-recording/value-objects/weight.js";
import * as _waterBalance from "../../domains/water-recording/value-objects/water-balance.js";
import * as _glass from "../../domains/water-recording/value-objects/glass.js";

export const pageView: views.WindowView = {
    redrawToLogin(): void {
        window.location.assign("/sign-in");
    },

    redrawForMainInteractions(): void {
        window.location.assign("/");
    },
}

export class ValidationCSSView implements views.ValidationView {
    constructor(
        private _element: HTMLElement,
        private _classNameWhenOk: string,
        private _classNameWhenNeutral: string,
    ) {}

    redrawOk(): void {
        this._element.className = this._classNameWhenOk;
    }

    redrawNeutral(): void {
        this._element.className = this._classNameWhenNeutral;
    }
}

export abstract class DefaultNotificationCSSView {
    constructor(
        protected _notificationElement: HTMLElement,
        protected _textElement: HTMLElement,
    ) {}

    redrawInvisible(): void {
        this._notificationElement.style.display = "none";
        this._textElement.innerText = "";
    }

    redrawTryAgainLater(): void {
        this._textElement.innerText = "Что то пошло не по плану, попробуйте когда нибудь потом!";
        this._redrawBad();
        this._redrawVisible();
    }

    protected _redrawVisible(): void {
        this._notificationElement.style.display = "unset";
    }

    protected _redrawBad(): void {
        this._notificationElement.className = "default-bad-notification";
    }

    protected _redrawNeutral(): void {
        this._notificationElement.className = "default-neutral-notification";
    }
}

export class LoginDefaultNotificationCSSView extends DefaultNotificationCSSView implements views.LoginNotificationView {
    redrawInvisible(): void {
        this._notificationElement.style.display = "none";
        this._textElement.innerText = "";
    }

    redrawNoUserWithUsername(_: _username.AnyUsername): void {
        this._textElement.innerText = "Пользователя с таким именем нет";
        this._redrawBad();
        this._redrawVisible();
    }

    redrawInvalidCredentials(_: _credentials.Credentials): void {
        this._textElement.innerText = "Неправильный пароль";
        this._redrawBad();
        this._redrawVisible();
    }

    redrawLastTimeThereWasNoUserNamed(_: _username.AnyUsername): void {
        this._textElement.innerText = "В прошлых попытках пользователя с таким именем не было";
        this._redrawNeutral();
        this._redrawVisible();
    }

    redrawLastTimeThereWasNoUserWithCredentials(_: _credentials.Credentials): void {
        this._textElement.innerText = "В прошлых попытках такой пароль не подошёл";
        this._redrawNeutral();
        this._redrawVisible();
    }

    redrawInvalidUsername(_: _username.AnyUsername): void {
        this._textElement.innerText = "Не может быть пользователя с таким именем";
        this._redrawBad();
        this._redrawVisible();
    }

    redrawInvalidPassword(_: _password.Password): void {
        this._textElement.innerText = "Не может быть пользователя с таким паролем";
        this._redrawBad();
        this._redrawVisible();
    }
}


export class RegistrationDefaultNotificationCSSView extends DefaultNotificationCSSView implements views.RegistrationNotificationView {
    redrawForUsernameHint(_: _username.AnyUsername): void {
        this._textElement.innerText = "Имя должно содержать хотя бы один символ";
        this._redrawNeutral();
        this._redrawVisible();
    }

    redrawUsernameTaken(_: _username.AnyUsername): void {
        this._textElement.innerText = "Имя уже занято";
        this._redrawBad();
        this._redrawVisible();
    }

    redrawForPasswordHint(_: _password.Password): void {
        let element1 = document.createElement("li");
        let element2 = document.createElement("li");
        let element3 = document.createElement("li");

        element1.innerText = "не менее 8 символов";
        element2.innerText = "любые цифры";
        element3.innerText = "буквы в нижнем и в верхнем регистрах";

        this._textElement.innerText = "Пароль должен иметь:";
        this._textElement.appendChild(element1);
        this._textElement.appendChild(element2);
        this._textElement.appendChild(element3);

        this._redrawNeutral();
        this._redrawVisible();
    }

    redrawForWeightHint(_: _weight.AnyWeight): void {
        this._textElement.innerText = "Вес должен быть целым положительным числом";
        this._redrawNeutral();
        this._redrawVisible();
    }

    redrawForTargetWaterBalanceHint(waterBalance: _waterBalance.AnyWaterBalance): void {}
    redrawForGlassHint(glass: _glass.AnyGlass): void,
}

export class PossiblyInvisibleCSSView implements views.PossiblyInvisibleView {
    constructor(private _element: HTMLElement) {}

    redrawVisible(): void {
        this._element.style.display = "unset";
    }

    redrawInvisible(): void {
        this._element.style.display = "none";
    }
}
