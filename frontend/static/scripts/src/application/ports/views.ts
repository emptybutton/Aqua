export interface WindowView {
    redrawForAuthorization(): void,
}

export interface TernaryView {
    redrawValid(): void,
    redrawNeutral(): void,
    redrawInvalid(): void,
}
