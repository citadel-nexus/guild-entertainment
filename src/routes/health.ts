export function healthCheck() {
  return {
    guild: 'entertainment',
    status: 'healthy',
    version: '0.1.0',
    nats_prefix: 'citadel.ent.*',
    timestamp: new Date().toISOString(),
  };
}
