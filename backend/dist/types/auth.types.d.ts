export interface User {
    id: string;
    email: string;
    role: 'admin' | 'user' | 'compliance_officer';
}
export interface AuthCredentials {
    email: string;
    password: string;
}
export interface AuthResponse {
    success: boolean;
    token?: string;
    user?: User;
    error?: string;
}
export interface JWTPayload {
    id: string;
    email: string;
    role: string;
    iat: number;
}
//# sourceMappingURL=auth.types.d.ts.map