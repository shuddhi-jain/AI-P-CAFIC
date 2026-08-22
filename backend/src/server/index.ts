// Import the framework and instantiate it
import Fastify from 'fastify'
const fastify = Fastify({
  logger: true
})
const users = []
// Declare a route
fastify.get('/', async function handler (request, reply) {
  return { hello: 'world' }
})
fastify.get('/userApi', async function handler (request, reply) {
  return { user: 'user' }
})
// Run the server!
try {
  await fastify.listen({ port: 8080 })
} catch (err) {
  fastify.log.error(err)
  process.exit(1)
}