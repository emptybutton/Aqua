export interface Timeout {
    doAfter(milliseconds: number, action: () => void): void,
    doNothing(): void,   
}
