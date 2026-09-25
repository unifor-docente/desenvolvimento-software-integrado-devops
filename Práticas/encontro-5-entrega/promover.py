"""Ensaio local de deploy e recuperação. Não faz build nem modifica schema.
Pré-requisitos: imagem candidata local e Docker/Compose; uso somente em laboratório.
"""
import argparse,json,os,subprocess,sys,urllib.request
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--imagem',required=True);p.add_argument('--versao',required=True);p.add_argument('--mensagem',required=True)
p.add_argument('--flag',choices=['true','false'],default='true')
p.add_argument('--projeto',default='e5-cd-local');p.add_argument('--porta',type=int,default=18087)
a=p.parse_args()
if not 1024<=a.porta<=65535:p.error('Porta deve estar entre 1024 e 65535')
lab=Path(__file__).resolve().parent;env=os.environ.copy();env.update(APP_IMAGE=a.imagem,FEATURE_BANNER=a.flag,PORTA_HOST=str(a.porta))
def run(args,check=True):
 r=subprocess.run(args,cwd=lab,env=env,text=True,capture_output=True)
 if check and r.returncode:raise RuntimeError(r.stderr.strip() or r.stdout.strip() or 'Comando falhou')
 return r
def compose(*args,check=True):return run(['docker','compose','-p',a.projeto,*args],check)
def get(path):
 with urllib.request.urlopen(f'http://localhost:{a.porta}'+path,timeout=8) as r:return json.load(r)
def smoke(version,message):
 return run([sys.executable,'verificar.py',f'http://localhost:{a.porta}',version,message],False)
# Congela a referência no conteúdo local já existente; não reconstrói nem baixa a candidata.
image_id=run(['docker','image','inspect','--format','{{.Id}}',a.imagem]).stdout.strip();env['APP_IMAGE']=image_id
compose('config','--quiet')
old=None;cid=compose('ps','-q','app').stdout.strip()
if cid:
 # Captura somente imagem e flag para recuperação. Não imprime o environment completo.
 obj=json.loads(run(['docker','inspect',cid]).stdout)[0]
 flags=[v.split('=',1)[1] for v in obj['Config']['Env'] if v.startswith('FEATURE_BANNER=')]
 old=dict(image=obj['Image'],flag=flags[0] if flags else 'false',version=get('/version')['version'],message=get('/mensagem')['mensagem'])
 assert smoke(old['version'],old['message']).returncode==0,'Referência atual não passou; investigar antes de promover'
report=dict(projeto=a.projeto,porta=a.porta,candidata=image_id,anterior=old['image'] if old else None)
try:
 if old:compose('up','-d','--no-deps','--no-build','--wait','app')
 else:compose('up','-d','--no-build','--wait')
 assert smoke(a.versao,a.mensagem).returncode==0,'Smoke funcional da candidata falhou'
 cid=compose('ps','-q','app').stdout.strip()
 actual=run(['docker','inspect','--format','{{.Image}}',cid]).stdout.strip()
 assert actual==image_id,'Instância não usa a imagem validada'
 report.update(resultado='promovida',imagem_em_execucao=actual)
 print(json.dumps(report,ensure_ascii=False,indent=2))
except Exception as exc:
 report.update(resultado='falha',motivo=str(exc),recuperacao='sem referência anterior; investigar')
 if old:
  env.update(APP_IMAGE=old['image'],FEATURE_BANNER=old['flag'])
  try:
   compose('up','-d','--no-deps','--no-build','--wait','app')
   assert smoke(old['version'],old['message']).returncode==0,'Smoke da recuperação falhou'
   report['recuperacao']='versão e flag anteriores restauradas e verificadas'
  except Exception as recovery:report['recuperacao']='FALHOU: '+str(recovery)
 print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(1)
