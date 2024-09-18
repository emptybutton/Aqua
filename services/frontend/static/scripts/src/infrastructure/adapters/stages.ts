import * as stages from "../../application/ports/stages.js"

export class InMemoryCurrentStage<StageT> implements stages.CurrentStage<StageT> {
    constructor(private _currentStage: StageT) {}

    is(stage: StageT): boolean {
        return this._currentStage === stage;
    }

    replaceWith(newStage: StageT): void {
        this._currentStage = newStage;
    }
}
