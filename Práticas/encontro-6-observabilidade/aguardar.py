"""Aguarda prontidão da API após iniciar db; não substitui a sonda funcional."""
import argparse,time,urllib.request,urllib.error
p=argparse.ArgumentParser();p.add_argument('--base',default='http://localhost:18086');a=p.parse_args()
for tentativa in range(30):
 try:
  with urllib.request.urlopen(a.base.rstrip('/')+'/health/ready',timeout=4) as r:
   if r.status==200:
    print('API pronta. Execute agora a sonda funcional de /visitas.');break
 except (urllib.error.URLError,TimeoutError,ConnectionError):pass
 time.sleep(1)
else:raise SystemExit('API não recuperou prontidão. Inspecione docker compose logs app db.')
