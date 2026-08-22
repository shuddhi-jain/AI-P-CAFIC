import type { FastifyInstance, FastifyRequest, FastifyReply } from 'fastify';
export declare function setupAuth(app: FastifyInstance): Promise<void>;
export declare function verifyToken(request: FastifyRequest, reply: FastifyReply): Promise<void>;
export declare function generateToken(app: FastifyInstance, payload: any): string;
//# sourceMappingURL=auth.d.ts.map