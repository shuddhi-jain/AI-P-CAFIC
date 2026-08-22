export class ApiError extends Error {
    statusCode;
    message;
    code;
    constructor(statusCode, message, code) {
        super(message);
        this.statusCode = statusCode;
        this.message = message;
        this.code = code;
        this.name = 'ApiError';
    }
}
export class ValidationError extends ApiError {
    constructor(message) {
        super(400, message, 'VALIDATION_ERROR');
        this.name = 'ValidationError';
    }
}
export class NotFoundError extends ApiError {
    constructor(message = 'Resource not found') {
        super(404, message, 'NOT_FOUND');
        this.name = 'NotFoundError';
    }
}
export class GenAIError extends ApiError {
    constructor(message) {
        super(500, message, 'GENAI_ERROR');
        this.name = 'GenAIError';
    }
}
export class StorageError extends ApiError {
    constructor(message) {
        super(500, message, 'STORAGE_ERROR');
        this.name = 'StorageError';
    }
}
//# sourceMappingURL=errors.js.map