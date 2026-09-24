"""Smoke funcional: Python 3 padrão; não instala dependências."""
import json, sys, urllib.request
base=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:18085'
version=sys.argv[2] if len(sys.argv)>2 else '1.0.0'
message=sys.argv[3] if len(sys.argv)>3 else 'Bem-vindos!'
def get(path):
 with urllib.request.urlopen(base+path,timeout=8) as r:
  assert r.status==200,(path,r.status)
  return json.load(r)
assert get('/health/ready')['status']=='ready'
assert get('/version')['version']==version,'Versão diferente da esperada'
assert get('/mensagem')['mensagem']==message,'Mensagem funcional incorreta'
assert isinstance(get('/visitas')['total'],int),'Contador ausente'
print('PASS: prontidão, versão, mensagem e leitura de dados')
