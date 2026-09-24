const http = require('node:http');
const release = require('./release.json');
const flag = process.env.FEATURE_BANNER === 'true';
const { Pool } = require('pg');
const pool = new Pool({ connectionString: process.env.DATABASE_URL, connectionTimeoutMillis: 2000, query_timeout: 3000 });
pool.on('error', err => console.error(JSON.stringify({ event: 'pool_error', code: err.code })));
const server = http.createServer(async (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  const send = (status, body) => { res.writeHead(status); res.end(JSON.stringify(body) + '\n'); };
  if (req.method === 'GET' && req.url === '/health/live') return send(200, { status: 'alive' });
  if (req.method === 'GET' && req.url === '/version') return send(200, { version: release.version, feature_banner: flag });
  if (req.method === 'GET' && req.url === '/mensagem') return send(200, { mensagem: flag ? release.banner : 'Bem-vindos!' });
  try {
    if (req.method === 'GET' && req.url === '/health/ready') {
      await pool.query('SELECT 1');
      return send(200, { status: 'ready' });
    }
    if (req.method === 'POST' && req.url === '/visitas') {
      const { rows } = await pool.query('UPDATE contador SET total = total + 1 WHERE id = 1 RETURNING total');
      return send(200, rows[0]);
    }
    if (req.method === 'GET' && req.url === '/visitas') {
      const { rows } = await pool.query('SELECT total FROM contador WHERE id = 1');
      return send(200, rows[0]);
    }
    return send(404, { error: 'Use GET /health/live, GET /health/ready, GET ou POST /visitas' });
  } catch (err) {
    console.error(JSON.stringify({ event: 'request_failed', code: err.code || 'DB_ERROR' }));
    return send(503, { error: 'Dependência indisponível; consulte os logs' });
  }
});
server.listen(Number(process.env.PORT || 3000), process.env.HOST || '0.0.0.0', () => {
  console.log(JSON.stringify({ event: 'listening', port: Number(process.env.PORT || 3000) }));
});
process.on('SIGTERM', () => {
  server.close(() => pool.end().then(() => process.exit(0)));
  setTimeout(() => process.exit(1), 8000).unref();
});
