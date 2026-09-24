const http = require('node:http');
const { randomUUID } = require('node:crypto');
const { performance } = require('node:perf_hooks');
const { Pool } = require('pg');
const version = '3.0.0-observabilidade';
const pool = new Pool({ connectionString: process.env.DATABASE_URL, connectionTimeoutMillis: 1500, query_timeout: 2500 });
const delay = Math.min(2000, Math.max(0, Number(process.env.DEMO_DELAY_MS) || 0));
const routes = new Set(['/health/live','/health/ready','/version','/visitas','/metrics']);
const counts = new Map();
const buckets = [0.01, 0.05, 0.1, 0.3, 1, 3];
const histogram = { count: 0, sum: 0, buckets: buckets.map(() => 0) };
const log = data => console.log(JSON.stringify({ timestamp: new Date().toISOString(), service: 'api-visitas', version, ...data }));
pool.on('error', err => log({ level: 'error', event: 'pool_error', error_code: err.code || 'DB_ERROR' }));
function record(method, route, status, seconds) {
  if (route !== '/visitas') return; // exclui probes, métricas e rotas desconhecidas
  const labels = `method="${method}",route="${route}",status="${status}"`;
  counts.set(labels, (counts.get(labels) || 0) + 1);
  if (method === 'GET') {
    histogram.count++; histogram.sum += seconds;
    buckets.forEach((limit,i) => { if (seconds <= limit) histogram.buckets[i]++; });
  }
}
function metrics() {
  const lines = ['# HELP aula_http_requests_total Respostas de /visitas desde a partida.', '# TYPE aula_http_requests_total counter'];
  for (const [labels, value] of counts) lines.push(`aula_http_requests_total{${labels}} ${value}`);
  lines.push('# HELP aula_http_request_duration_seconds Duracao de GET /visitas no servidor.', '# TYPE aula_http_request_duration_seconds histogram');
  buckets.forEach((limit,i) => lines.push(`aula_http_request_duration_seconds_bucket{le="${limit}"} ${histogram.buckets[i]}`));
  lines.push(`aula_http_request_duration_seconds_bucket{le="+Inf"} ${histogram.count}`);
  lines.push(`aula_http_request_duration_seconds_sum ${histogram.sum}`);
  lines.push(`aula_http_request_duration_seconds_count ${histogram.count}`);
  return lines.join('\n')+'\n';
}
const server = http.createServer(async (req,res) => {
  const start = performance.now();
  const requestId = randomUUID();
  const pathname = (req.url || '/').split('?')[0];
  const route = routes.has(pathname) ? pathname : 'other';
  const method = ['GET','POST'].includes(req.method) ? req.method : 'OTHER';
  let dependencyMs = 0, errorCode;
  res.setHeader('X-Request-Id', requestId);
  const send = (status, body, type='application/json') => {
    const duration = performance.now()-start;
    record(method,route,status,duration/1000);
    res.writeHead(status, {'Content-Type': type});
    res.end(type === 'application/json' ? JSON.stringify(body)+'\n' : body);
    if (route !== '/metrics') log({ level: status >= 500 ? 'error' : 'info', event: 'http_request', request_id: requestId, method, route, status, duration_ms: Number(duration.toFixed(2)), dependency_ms: Number(dependencyMs.toFixed(2)), ...(errorCode ? {error_code:errorCode} : {}) });
  };
  const query = async sql => {
    const t = performance.now();
    try {
      if (delay) await new Promise(resolve => setTimeout(resolve,delay));
      return await pool.query(sql);
    } finally { dependencyMs += performance.now()-t; }
  };
  if (method === 'GET' && route === '/metrics') return send(200,metrics(),'text/plain; version=0.0.4');
  if (method === 'GET' && route === '/version') return send(200,{version, demo_delay_ms:delay});
  if (method === 'GET' && route === '/health/live') return send(200,{status:'alive'});
  try {
    if (method === 'GET' && route === '/health/ready') { await query('SELECT 1'); return send(200,{status:'ready'}); }
    if (method === 'GET' && route === '/visitas') {
      const {rows} = await query('SELECT total FROM contador WHERE id = 1');
      if (!rows[0]) throw Object.assign(new Error('Contador ausente'),{code:'COUNTER_MISSING'});
      return send(200,rows[0]);
    }
    if (method === 'POST' && route === '/visitas') {
      const {rows} = await query('UPDATE contador SET total = total + 1 WHERE id = 1 RETURNING total');
      if (!rows[0]) throw Object.assign(new Error('Contador ausente'),{code:'COUNTER_MISSING'});
      return send(200,rows[0]);
    }
    return send(404,{error:'Rota não encontrada'});
  } catch (err) {
    errorCode = err.code || 'DB_ERROR';
    return send(503,{error:'Dependência indisponível',request_id:requestId});
  }
});
server.listen(Number(process.env.PORT || 3000),process.env.HOST || '0.0.0.0', () => log({level:'info',event:'listening',port:Number(process.env.PORT || 3000)}));
process.on('SIGTERM', () => {
  server.close(() => pool.end().then(() => process.exit(0)));
  setTimeout(() => process.exit(1),8000).unref();
});
