import jwt from '@fastify/jwt';
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-this';
export async function setupAuth(app) {
    // Register JWT plugin
    await app.register(jwt, {
        secret: JWT_SECRET
    });
}
export async function verifyToken(request, reply) {
    try {
        await request.jwtVerify();
    }
    catch (error) {
        reply.status(401).send({
            success: false,
            error: 'Unauthorized - Invalid or missing token'
        });
    }
}
export function generateToken(app, payload) {
    return app.jwt.sign(payload);
}
//# sourceMappingURL=auth.js.map