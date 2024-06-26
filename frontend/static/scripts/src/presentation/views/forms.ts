import { ValidationError } from "../../domain/errors.js";

export class FormFieldView<ElementT extends HTMLElement = HTMLElement> {
    private _classNameDuringValidValue: string;
    private _classNameDuringInvalidValue: string;

    constructor(
        readonly element: ElementT,
        classNameDuringValidValue?: string,
        classNameDuringInvalidValue?: string,
    ) {
        this._classNameDuringValidValue = classNameDuringValidValue ?? element.className;
        this._classNameDuringInvalidValue = classNameDuringInvalidValue ?? element.className;
    }

    redrawValid(): void {
        this.element.className = this._classNameDuringValidValue;
    }

    redrawInvalid(): void {
        this.element.className = this._classNameDuringInvalidValue;
    }
}

export class FormView<ElementT extends HTMLElement = HTMLElement> {
    private _classNameWhenReady: string;
    private _classNameDuringRunning: string;
    private _classNameDuringUnknownError: string;

    constructor(
        readonly element: ElementT,
        classNameDuringRunning?: string,
        classNameDuringUnknownError?: string,
    ) {
        this._classNameWhenReady = element.className;
        this._classNameDuringRunning = classNameDuringRunning ?? element.className;
        this._classNameDuringUnknownError = classNameDuringUnknownError ?? element.className;
    }

    redrawByUnknownError(): void {
        this.element.className = this._classNameDuringUnknownError;
    }

    redrawRunning(): void {
        this.element.className = this._classNameDuringRunning;
    }

    redrawReady(): void {
        this.element.className = this._classNameWhenReady;
    }
}

export function redrawByValidation<ResultT>(
    view: FormFieldView,
    validation: () => ResultT,
): ResultT | undefined {
    try {
        var validationResult = validation();
    } catch (error) {
        if (!(error instanceof ValidationError))
            throw error;

        view.redrawInvalid();
        return;
    }

    view.redrawValid();
    return validationResult;
}
