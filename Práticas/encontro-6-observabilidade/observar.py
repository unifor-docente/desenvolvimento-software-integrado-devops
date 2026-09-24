"""Sonda HTTP serial e finita, com resumo verificável. Usa somente Python 3 padrão."""
import argparse, json, math, time, urllib.request, urllib.error, sys
p=argparse.ArgumentParser()
p.add_argument('--base',default='http://localhost:18086')
p.add_argument('--amostras',type=int,default=10)
p.add_argument('--intervalo',type=float,default=.1)
p.add_argument('--esperado',type=int,choices=[200,503],default=200)
a=p.parse_args()
if not 1<=a.amostras<=100 or not 0<=a.intervalo<=5:p.error('Use 1–100 amostras e intervalo de 0–5 segundos')
rows=[]
for i in range(a.amostras):
 start=time.perf_counter();status=None;payload={};request_id=None;problem=None
 try:
  try: response=urllib.request.urlopen(a.base.rstrip('/')+'/visitas',timeout=6)
  except urllib.error.HTTPError as exc:response=exc
  with response:
   status=response.code;request_id=response.headers.get('X-Request-Id')
   try:payload=json.load(response)
   except (json.JSONDecodeError,UnicodeDecodeError):problem='resposta_json_invalida'
 except (urllib.error.URLError,TimeoutError,ConnectionError) as exc:problem=type(exc).__name__
 elapsed=(time.perf_counter()-start)*1000
 good=status==200 and isinstance(payload,dict) and isinstance(payload.get('total'),int) and not isinstance(payload.get('total'),bool)
 row=dict(amostra=i+1,status=status,boa=good,duration_ms=round(elapsed,2),request_id=request_id)
 if problem:row['erro']=problem
 rows.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
 if i<a.amostras-1:time.sleep(a.intervalo)
ordered=sorted(r['duration_ms'] for r in rows)
summary=dict(amostras=len(rows),boas=sum(r['boa'] for r in rows),falhas=sum(not r['boa'] for r in rows),sucesso_pct=100*sum(r['boa'] for r in rows)/len(rows),p95_ms=ordered[math.ceil(.95*len(rows))-1],metodo_percentil='nearest-rank',origem='sonda cliente serial; inclui rede e leitura da resposta')
print(json.dumps({'resumo':summary},ensure_ascii=False),flush=True)
# --esperado=503 confirma a falha provocada; não significa que o serviço está saudável.
if any(r['status']!=a.esperado or (a.esperado==200 and not r['boa']) for r in rows):sys.exit(1)
