import * as views from "../../application/ports/views.js";

export const pageView: views.WindowView = {
    redrawForAuthorization(): void {
        window.location.assign("/sign-in");
    },
}

export class TernaryCSSView<ElementT extends HTMLElement = HTMLElement> implements views.TernaryView {
    constructor(
        private _element: ElementT,
        private _classNameWhenValid: string,
        private _classNameWhenInvalid: string,
        private _classNameWhenNeutral: string,
    ) {}

    redrawValid(): void {
        this._element.className = this._classNameWhenValid;
    }

    redrawInvalid(): void {
        this._element.className = this._classNameWhenInvalid;
    }

    redrawNeutral(): void {
        this._element.className = this._classNameWhenNeutral;
    }
}
