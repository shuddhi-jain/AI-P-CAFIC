export declare class ApiError extends Error {
    statusCode: number;
    message: string;
    code?: string | undefined;
    constructor(statusCode: number, message: string, code?: string | undefined);
}
export declare class ValidationError extends ApiError {
    constructor(message: string);
}
export declare class NotFoundError extends ApiError {
    constructor(message?: string);
}
export declare class GenAIError extends ApiError {
    constructor(message: string);
}
export declare class StorageError extends ApiError {
    constructor(message: string);
}
//# sourceMappingURL=errors.d.ts.map